from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSortTracker:
    def __init__(self, config):
        self.tracker = DeepSort(
            max_age=config['deep_sort']['max_age'],
            n_init=config['deep_sort']['n_init']
        )

    def update_tracks(self, detections, frame):
        return self.tracker.update_tracks(detections, frame=frame)
