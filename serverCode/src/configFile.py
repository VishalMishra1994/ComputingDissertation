from pathlib import Path

SERVER_IP = "100.94.90.37"
deviceName = "TestCar"

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
FacesFolder = parent_dir / "Recognised_Faces"
FacesFolder.mkdir(parents=True, exist_ok=True)