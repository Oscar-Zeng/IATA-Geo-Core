# ✈️ IATA-Geo-Core: MCP Aviation Distance Engine

**IATA-Geo-Core** is a high-precision Model Context Protocol (MCP) server designed for aviation-specific geospatial calculations. It provides a reliable interface for AI agents to query airport information and calculate **Great Circle** distances between thousands of commercial airports globally using 3-letter IATA codes.

---

## 🌟 Key Features

- **FFP Industry Standard**: Calculates distances in **Statute Miles**, the universal standard for Airline Frequent Flyer Program (FFP) accruals.
- **Curated Dataset**: Powered by a refined database of 4,000+ active commercial airports (Large, Medium, and Scheduled Service hubs).
- **Precision Math**: Implements the **Haversine Formula** for accurate spherical distance calculation.
- **MCP Native**: Built to integrate seamlessly with **Claude Desktop**, Cursor, and other MCP-compatible AI environments.

---

## 📂 Project Structure

```text
IATA-Geo-Core/
├── data/               # Refined airport database (iata_geo_core.csv)
├── scripts/            # Core logic (calculator.py, refine_data.py)
├── mcp_server.py       # MCP Server entry point (STDIO transport)
└── README.md           # Documentation
```

---

## 🛠️ Installation & Data Setup

### 1. Initialize Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mcp pandas
```

### 2. Generate Core Data

Run the refinement script to fetch and process the latest global airport data:

```bash
python3 scripts/refine_data.py
```

---

## 🚀 Claude Desktop Configuration

To enable these tools in Claude Desktop, add the following entry to your configuration file:

**File Path:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "iata-geo-core": {
      "command": "/Users/<YOUR_USERNAME>/Documents/IATA-Geo-Core/.venv/bin/python3",
      "args": [
        "/Users/<YOUR_USERNAME>/Documents/IATA-Geo-Core/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/<YOUR_USERNAME>/Documents/IATA-Geo-Core"
      }
    }
  }
}
```

---

## 🔧 Tools Provided

### `get_airport_distance`

Calculates the Great Circle distance between two airports.

- **Input:** `origin` (e.g., `"PEK"`), `destination` (e.g., `"JFK"`).
- **Returns:** Distance in statute miles (float).
- **Example Query:** *"How many miles from London Heathrow to Singapore Changi?"*

---

## 📐 Technical Specifications

- **Algorithm:** Haversine Formula.
- **Earth Radius ($r$):** Using $3958.8$ miles (Mean radius).
- **Formula:**

$$d = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos\phi_1 \cos\phi_2 \sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$

- **Data Source:** Refined from [OurAirports](https://ourairports.com/) Open Data.

---

## 📜 License

MIT License. Created for the AeroAccrual Ecosystem.
