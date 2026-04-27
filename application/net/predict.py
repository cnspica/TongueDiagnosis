import os
import queue
import tempfile
import torch
from PIL import Image
import numpy as np
from yolov5 import load
from segment_anything import sam_model_registry,SamPredictor
from application.net.model.resnet import ResNetPredictor
from application.config import Settings


class TonguePredictor:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,
                 yolo_path='application/net/weights/yolov5.pt',
                 sam_path='application/net/weights/sam_vit_b_01ec64.pth',
                 resnet_path=[
                     'application/net/weights/tongue_color.pth',
                     'application/net/weights/tongue_coat_color.pth',
                     'application/net/weights/thickness.pth',
                     'application/net/weights/rot_and_greasy.pth'
                 ]
                 ):
        if self._initialized:
            return
        self.device = torch.device('cpu')
        self.yolo = load(yolo_path, device='cpu')
        self.sam = sam_model_registry["vit_b"](checkpoint=sam_path)
        self.resnet = ResNetPredictor(resnet_path)
        self.queue = queue.Queue()
        TonguePredictor._initialized = True

    def __predict(self, img, record_id, fun, img_save_path=None):
        print(f"[CROP-DEBUG] __predict called with img_save_path={img_save_path}")
        predict_img = Image.open(img)
        self.yolo.eval()
        print("Tongue positioning")
        with torch.no_grad():
            pred = self.yolo(predict_img)
        if len(pred.xyxy[0]) < 1:
            fun(event_id=record_id,
                tongue_color=None,
                coating_color=None,
                tongue_thickness=None,
                rot_greasy=None,
                code=201)
            print("The picture is not legal and has no tongue.")
            return
        elif len(pred.xyxy[0]) > 1:
            fun(event_id=record_id,
                tongue_color=None,
                coating_color=None,
                tongue_thickness=None,
                rot_greasy=None,
                code=202)
            print("The picture is not legal. There are too many tongues.")
            return
        print("Tongue segmentation")
        with torch.no_grad():
            x1, y1, x2, y2 = (
                pred.xyxy[0][0, 0].item(), pred.xyxy[0][0, 1].item(), pred.xyxy[0][0, 2].item(),
                pred.xyxy[0][0, 3].item())
            predictor = SamPredictor(sam_model=self.sam)
            predictor.set_image(np.array(predict_img))
            masks, _, _ = predictor.predict(box=np.array([x1, y1, x2, y2]))
            original_img = np.array(predict_img)
            masks = np.transpose(masks, (1,2,0))
            # 使用最佳 mask（通常第0个是最佳）进行抠图
            best_mask = masks[:, :, 0:1]  # 取第一个 mask
            pred_masked = original_img * best_mask
            # 裁剪到 bbox 区域
            cropped_img = Image.fromarray(pred_masked).crop((x1, y1, x2, y2)).convert("RGB")
            
            # 保存抠好的舌头图片
            cropped_img_path = None
            if img_save_path:
                try:
                    # 生成抠图文件名：原图名_crop.ext
                    base, ext = os.path.splitext(img_save_path)
                    cropped_img_path = f"{base}_crop{ext}"
                    cropped_img.save(cropped_img_path, quality=95)
                    print(f"[CROP] Saved cropped tongue image: {cropped_img_path}")
                except Exception as e:
                    print(f"[CROP] Failed to save cropped image: {e}")
                    cropped_img_path = None
            
            result = np.array(cropped_img)
        result = self.resnet.predict(result)
        print("Tongue analysis")
        predict_result = {
            "code": 0,
            'tongue_color': result[0],
            'tongue_coat_color': result[1],
            'thickness': result[2],
            'rot_and_greasy': result[3]
        }
        fun(event_id=record_id,
            tongue_color=result[0],
            coating_color=result[1],
            tongue_thickness=result[2],
            rot_greasy=result[3],
            code=1,
            cropped_img_path=cropped_img_path)
        return predict_result

    def predict(self, img, record_id, fun, img_save_path=None):
        try:
            img.seek(0)
            tmpfile = tempfile.SpooledTemporaryFile()
            content = img.read()
            tmpfile.write(content)
            print(f"[CROP] predict() called with img_save_path={img_save_path}")
            self.queue.put((tmpfile, record_id, fun, img_save_path))
            img.seek(0)
            return {"code": 0}
        except Exception as e:
            print(f"[CROP] predict() error: {e}")
            return {"code": 3}

    def main(self):
        while True:
            if self.queue.empty():
                continue
            item = self.queue.get()
            img, record_id, fun = item[0], item[1], item[2]
            img_save_path = item[3] if len(item) > 3 else None
            try:
                self.__predict(img, record_id, fun, img_save_path)
            except Exception as e:
                print(e)
                fun(event_id=record_id,
                    tongue_color=None,
                    coating_color=None,
                    tongue_thickness=None,
                    rot_greasy=None,
                    code=203)
            finally:
                img.close()
