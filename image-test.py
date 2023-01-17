import os
from mmdet.apis import init_detector, inference_detector

config_name = 'swin-peach'
config_file = f'configs/swin/{config_name}.py'
checkpoint_file = f'work_dirs/{config_name}/latest.pth'

model = init_detector(config_file, checkpoint_file, device='cuda:1')

ROOT_DIR = '../minmax'
# ROOT_DIR = '../Straight2_test_coco/JPEGImages'  

for file in os.listdir(ROOT_DIR):
    print(f'file: {file}')
    img = f'{ROOT_DIR}/{file}'
    result = inference_detector(model, img)

    model.show_result(img, result, out_file=f'/home/ssomda/{file}', score_thr=0.5)
#file = '210624-t1-01.JPG'
#img = f'../test/{file}'
#result = inference_detector(model, img)
#model.show_result(img, result, out_file=f'result_test/{file}', score_thr=0.5, mask_color=(249,147,113))
