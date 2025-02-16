import torch
import numpy as np

def check_gpu_availability():
    """
    Check if GPU is available and return device info
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        device_props = {
            "name": torch.cuda.get_device_name(0),
            "memory_total": torch.cuda.get_device_properties(0).total_memory,
            "memory_available": torch.cuda.memory_allocated(0),
            "compute_capability": torch.cuda.get_device_capability(0)
        }
        return True, device, device_props
    return False, torch.device("cpu"), None

def optimize_memory_usage():
    """
    Optimize GPU memory usage for graph operations
    """
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.memory.empty_cache()
        return True
    return False

def get_performance_metrics():
    """
    Get GPU performance metrics
    """
    if not torch.cuda.is_available():
        return {"error": "GPU not available"}
    
    return {
        "memory_allocated": torch.cuda.memory_allocated(0),
        "memory_cached": torch.cuda.memory_reserved(0),
        "max_memory_allocated": torch.cuda.max_memory_allocated(0),
        "utilization": torch.cuda.utilization(0)
    }

def batch_to_gpu(data, batch_size=1000):
    """
    Transfer data to GPU in batches to prevent memory overflow
    """
    if not torch.cuda.is_available():
        return data
    
    if isinstance(data, np.ndarray):
        data = torch.from_numpy(data)
    
    if len(data) <= batch_size:
        return data.cuda()
    
    batches = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size].cuda()
        batches.append(batch)
    
    return torch.cat(batches)

if __name__ == "__main__":
    # Test GPU availability and print info
    available, device, props = check_gpu_availability()
    if available:
        print("GPU Available:")
        print(f"Device: {props['name']}")
        print(f"Memory: {props['memory_total'] / 1e9:.2f} GB")
        print(f"Compute Capability: {props['compute_capability']}")
    else:
        print("GPU not available, using CPU")
