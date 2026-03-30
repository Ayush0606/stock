"""
Async task utilities for background operations
"""
import asyncio
import logging
from typing import Callable, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class AsyncTask:
    """Manage async background tasks"""
    
    def __init__(self, task_id: str, task_name: str, status: str = "pending"):
        self.task_id = task_id
        self.task_name = task_name
        self.status = status  # pending, running, completed, failed
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class TaskManager:
    """Manage async tasks"""
    
    def __init__(self):
        self.tasks = {}
    
    async def execute_task(
        self,
        task_id: str,
        task_name: str,
        func: Callable,
        *args,
        **kwargs
    ) -> AsyncTask:
        """Execute an async task"""
        task = AsyncTask(task_id, task_name, status="running")
        task.started_at = datetime.now()
        self.tasks[task_id] = task
        
        try:
            logger.info(f"Starting task: {task_name} (ID: {task_id})")
            
            # Check if coroutine or regular function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = await asyncio.to_thread(func, *args, **kwargs)
            
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.now()
            
            logger.info(f"Completed task: {task_name} (ID: {task_id})")
            
        except Exception as e:
            task.error = str(e)
            task.status = "failed"
            task.completed_at = datetime.now()
            logger.error(f"Failed task: {task_name} (ID: {task_id}) - {str(e)}")
        
        return task
    
    def get_task(self, task_id: str) -> Optional[AsyncTask]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> list:
        """List all tasks"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def clear_completed(self) -> int:
        """Clear completed tasks"""
        initial_count = len(self.tasks)
        self.tasks = {
            k: v for k, v in self.tasks.items()
            if v.status not in ["completed", "failed"]
        }
        return initial_count - len(self.tasks)


# Global task manager
_task_manager = TaskManager()


async def run_async_task(
    task_id: str,
    task_name: str,
    func: Callable,
    *args,
    **kwargs
) -> AsyncTask:
    """Run an async task and track it"""
    return await _task_manager.execute_task(task_id, task_name, func, *args, **kwargs)


def get_task_status(task_id: str) -> Optional[dict]:
    """Get task status"""
    task = _task_manager.get_task(task_id)
    return task.to_dict() if task else None


def list_all_tasks() -> list:
    """List all tasks"""
    return _task_manager.list_tasks()


# Example usage:
"""
from app.utils.async_tasks import run_async_task
import uuid

async def heavy_task(symbol: str):
    # Simulate long-running operation
    await asyncio.sleep(5)
    return f"Processed {symbol}"

# Start task
task_id = str(uuid.uuid4())
await run_async_task(task_id, "Process Stock", heavy_task, "INFY.NS")

# Check status
status = get_task_status(task_id)
print(status)
"""
