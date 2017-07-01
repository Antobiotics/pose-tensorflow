from pose.dataset.pose_dataset import PoseDataset


def create(cfg):
    dataset_type = cfg.dataset_type
    if dataset_type == "mpii":
        from pose.dataset.mpii import MPII
        data = MPII(cfg)
    elif dataset_type == "coco":
        from pose.dataset.mscoco import MSCOCO
        data = MSCOCO(cfg)
    elif dataset_type == "penn_action":
        from pose.dataset.penn_action import PennAction
        data = PennAction(cfg)
    elif dataset_type == "default":
        data = PoseDataset(cfg)
    else:
        raise Exception("Unsupported dataset_type: \"{}\"".format(dataset_type))
    return data
