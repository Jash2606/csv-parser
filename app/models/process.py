from datetime import datetime
from app.database import get_db

class Process:
    @classmethod
    def get_collection(cls):
        db = get_db()
        return db.processes

    @classmethod
    def create_process(cls, task_id, status):
        collection = cls.get_collection()
        process_entry = {
            "task_id": task_id,
            "status": status,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        collection.insert_one(process_entry)

    @classmethod
    def update_status(cls, task_id, status):
        collection = cls.get_collection()
        collection.update_one(
            {"task_id": task_id},
            {"$set": {"status": status, "updated_at": datetime.now()}}
        )
    
    @classmethod
    def get_process_by_task_id(cls, task_id):
        collection = cls.get_collection()
        process = collection.find_one({"task_id": task_id})
        if process:
            process["_id"] = str(process["_id"])
            return process
        return None

    @classmethod
    def get_all_processes(cls):
        collection = cls.get_collection()
        processes = list(collection.find().sort("created_at", -1))
        for process in processes:
            process["_id"] = str(process["_id"])
        return processes

