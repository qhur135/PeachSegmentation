_base_ = 'mask_rcnn_swin-t-p4-w7_fpn_fp16_ms-crop-3x_coco.py'
pretrained = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.0/swin_tiny_patch4_window7_224.pth'  # noqa
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=1),
        mask_head=dict(num_classes=1)))
# Modify dataset related settings
dataset_type = 'PeachDataset'
classes = ('peach',)
data = dict(
    train=dict(
        img_prefix='../peach-data/train/',
        classes=classes,
        ann_file='../peach-data/train.json'),
    val=dict(
        img_prefix='../peach-data/val/',
        classes=classes,
        ann_file='../peach-data/val.json'),
    test=dict(
        img_prefix='../peach-data/test/',
        classes=classes,
        ann_file='../peach-data/test.json'))
