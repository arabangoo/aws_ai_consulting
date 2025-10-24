from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="Standalone FastAPI MCP Server")

# --- CORS 미들웨어 설정 ---
origins = [
    "*"  # 테스트 목적으로 모든 출처를 허용합니다. 
         # 보안을 위해 실제 서비스에서는 특정 도메인만 허용하는 것이 좋습니다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드(GET, POST 등)를 허용합니다.
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용합니다.
)

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "standalone-mcp/1.0"

class ForecastRequest(BaseModel):
    latitude: float
    longitude: float

class AlertsRequest(BaseModel):
    state: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/mcp/get_forecast")
async def get_forecast(req: ForecastRequest):
    points_url = f"{NWS_API_BASE}/points/{req.latitude},{req.longitude}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            points_data_res = await client.get(points_url, headers=headers, timeout=30.0)
            points_data_res.raise_for_status()  # 2xx 상태 코드가 아니면 예외 발생
            
            points_data = points_data_res.json()
            forecast_url = points_data.get("properties", {}).get("forecast")
            if not forecast_url:
                raise HTTPException(status_code=404, detail="Forecast URL not found in location data.")

            forecast_data_res = await client.get(forecast_url, headers=headers, timeout=30.0)
            forecast_data_res.raise_for_status()

            forecast_data = forecast_data_res.json()
            periods = forecast_data.get("properties", {}).get("periods", [])
            return {"forecast": periods[:5]}  # 상위 5개만 반환

        except httpx.HTTPStatusError as e:
            # 외부 API 호출 실패 시 에러 처리
            raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching data from NWS: {e.response.text}")
        except Exception as e:
            # 기타 예외 처리
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.post("/mcp/get_alerts")
async def get_alerts(req: AlertsRequest):
    url = f"{NWS_API_BASE}/alerts/active/area/{req.state.upper()}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            data_res = await client.get(url, headers=headers, timeout=30.0)
            data_res.raise_for_status()
            
            data = data_res.json()
            features = data.get("features", [])
            return {"alerts": features}

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching alerts from NWS: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")