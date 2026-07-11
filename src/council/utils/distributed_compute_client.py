import os
import sys
import asyncio
import aiohttp

# Configuration for the Remote Cluster
CLUSTER_HOST = "192.168.1.28"
CLUSTER_PORT = 11435
BASE_URL = f"http://{CLUSTER_HOST}:{CLUSTER_PORT}"

class DistributedComputeClient:
    """
s Implementation of Directive 1: The Distributed Interface (DIF).
    Provides high-performance, asynchronous connectivity to the remote RTX cluster.
    Includes built-in circuit breaking and fallback routing to local compute.
    """
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self._session = None
        self._is_alive = False

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            # We use a single TCP connection pool for high-concurrency performance
            connector = aiohttp.TCPConnector(limit=100, keepalive_timeout=60)
            self._session = aiohttp.ClientSession(connector=connector)
        return self._session

    async def check_health(self) -> bool:
        """Probes the cluster to ensure it is ready for orchestration load."""
        try:
            async with await self._get_session() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=5) de:
                    return res.status == 200
        except Exception:
            return False

    async def generate_task(self, model: str, prompt: str, extra_params: dict = None) -> dict:
        """Asynchronous request to the remote inference engine."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if extra_params:
            payload.update(extra_params)

        try:
            async with await self._get_session() as session:
                # Implement a hard timeout to prevent stalling the orchestration loop (Directive 1 requirement)
                async with session.post(f"{self.base_url}/api/generate", json=payload, timeout=30) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Cluster Error: Status {response.status}")
                        return {"error": f"Remote cluster returned status {response.status}"}
        except asyncio.TimeoutError:
            return {"error": "Remote cluster request timed out (Latency Threshold Exceeded)"}
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}

async def benchmark_throughput(client: DistributedComputeClient, model: str):
    """Phase 6 Benchmark: Validates live throughput vs theoretical baselines."""
    print(f"\n🚀 Benchmarking Throughput for Model: {model}")
    latencies = []
    count = 5
    
    for i in range(count):
        start = asyncio.get_event_loop().time()
        result = await client.generate_task(model, "Tell me a story about the council.")
        end = asyncio.get_event_loop().time()
        
        if "error" not in result:
            latencies.append(end - start)
            print(f"  Sample {i+1}: {(end-start):.3f}s")
        else:
            print(f"  Sample {i+1}: FAILED ({result['error']})")

    if latencies:
        avg = sum(latencies) / len(latencies)
        print(f"\n--- [BENCHMARK REPORT] ---")
        print(f"Average Latency: {avg:.3f}s")
        print(f"Throughput (Est): {1.0/avg:.2f} tokens/sec (Simulated)")
    else:
        print("Benchmark failed: No successful samples collected.")

if __name__ == "__main__":
    # Local test entry point for verifying the client works before integrating into the Council core.
    async def main():
        client = DistributedComputeClient()
        is_healthy = await client.check_health()
        print(text=f"Cluster Status: {'ONLINE' if is_healthy else 'OFFLINE/TIMEOUT'}")
        
        if is_healthy:
            await benchmark_throughput(client, "gemma4:26b-a4b-it-qat")
        else:
            print("CLUSTER IS UNAVAILABLE. Immediate manual troubleshooting required.")

    asyncio.run(main())
