from dotenv import load_dotenv
from run import create_app


load_dotenv()

flask_app = create_app()

from app.database import get_db_connection
mongo_client, mongo_db = get_db_connection()

from app.zmq_instance import get_pull_socket
from app.tasks import process_csv_task
from app.models.process import Process
def main():
    """
    Main worker function that listens for tasks and processes them
    """
    print("Starting ZeroMQ worker...")
    socket, context = get_pull_socket()
    
    # Map of task names to functions
    task_map = {
        'process_csv_task': process_csv_task,
    }
    
    try:
        with flask_app.app_context():
            while True:
                print("Waiting for tasks...")
                task_data = socket.recv_json()
                
                task_id = task_data.get('task_id')
                task_name = task_data.get('task')
                kwargs = task_data.get('kwargs', {})
                
                print(f"Received task: {task_name} (ID: {task_id})")
                Process.create_process(task_id, "processing")
                # Execute the task
                if task_name in task_map:
                    try:
                        print(f"Processing task {task_id}...")
                        task_function = task_map[task_name]
                        result = task_function(**kwargs, task_id=task_id)
                        print(f"Task {task_id} completed successfully")
                        print(f"Result: {result}")
                        Process.update_status(task_id, "completed")
                    except Exception as e:
                        print(f"Error executing task {task_id}: {str(e)}")
                        Process.update_status(task_id, "failed")
                else:
                    print(f"Unknown task: {task_name}")
                    Process.update_status(task_id, "failed")
    except KeyboardInterrupt:
        print("Worker shutting down...")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()
