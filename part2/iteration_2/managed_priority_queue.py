from Queue import PriorityQueue
from multiprocessing import managers

def shared_priority_queue():
    class MyManager(managers.SyncManager):
        pass
    MyManager.register("PriorityQueue", PriorityQueue)  # Register a shared PriorityQueue
    def multiprocess_manager():
        m = MyManager()
        m.start()
        return m
    priority_queue_manager = multiprocess_manager()
    return priority_queue_manager.PriorityQueue() 
    