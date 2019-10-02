from lib.dataset.dataietr import FaceKeypointDataIter
from train_config import config
import tensorflow as tf


from lib.core.model.simpleface import SimpleFace
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import cv2
from train_config import config as cfg
cfg.TRAIN.batch_size=1

ds = FaceKeypointDataIter(cfg.DATA.root_path,cfg.DATA.train_txt_path,False)
train_dataset = tf.data.Dataset.from_generator(ds,
                                               output_types=(tf.float32, tf.float32),
                                               output_shapes=([None, None, None], [cfg.MODEL.out_channel]))


face=SimpleFace()

# model='./model/epoch_7_val_loss63.637318'
# face.load_weights(model)


for images, labels in train_dataset:
    img_show = np.array(images)

    images=np.expand_dims(images,axis=0)

    res=face.inference(images)
    print(res)

    img_show=img_show.astype(np.uint8)

    img_show=cv2.cvtColor(img_show, cv2.COLOR_BGR2RGB)

    landmark = np.array(res[0][0:136]).reshape([-1, 2])

    for _index in range(res.shape[0]):
        x_y = res[_index]
        cv2.circle(img_show, center=(int(x_y[0] * config.MODEL.hin),
                                     int(x_y[1] * config.MODEL.win)),
                   color=(255, 122, 122), radius=1, thickness=2)

    cv2.imshow('tmp',img_show)
    cv2.waitKey(0)
