# (C) Copyright 2023 João Pedro de S. T. Costa; under Apache 2.0 License. Read EOF for more information.
from pdf_lib import *
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import cv2


class MODEL_FACEBOOK_DETR_RESNET_101:
    """
    DEtection TRansformer (DETR) model trained end-to-end on COCO 2017 object detection (118k annotated images).
    It was introduced in the paper End-to-End Object Detection with Transformers by Carion et al.
    See https://github.com/facebookresearch/detr and https://arxiv.org/abs/2005.12872
    """
    def __init__(self, pdf_lib_instance: PdfUtils):
        self.image = pdf_lib_instance.finalDwgImage

    def run(self):
        try:
            processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101", revision="no_timm")
            model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101", revision="no_timm")

            inputs = processor(images=self.image, return_tensors="pt")
            outputs = model(**inputs)

            # convert outputs (bounding boxes and class logits) to COCO API
            target_sizes = torch.tensor([self.image.size[::-1]])
            results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.1)[0]

            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = [round(i, 2) for i in box.tolist()]
                print(
                    f"Detected {model.config.id2label[label.item()]} with confidence "
                    f"{round(score.item(), 3)} at location {box}")

            print("model inference done :))")

        except Exception as e:
            print("[ERROR] something gone wrong and inference failed~~")
class MODEL_YOLOS_SMALL_300:
    pass



#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
