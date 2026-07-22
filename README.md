## DB Manager

## Architecture

```text
┌─────────────────────────────────────────────┐
│ CLI Layer                                   │
│ main.py, cli.py                             │
│ Parses & validates command-line input       │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ Orchestration Layer                         │
│ main.py                                     │
│ Load → Query → Export                       │
└─────────────────────────────────────────────┘
         │             │             │
         ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Load         │ │ Query        │ │ Export       │
│ loader.py    │ │ query.py     │ │ export.py    │
│ Loads JSON   │ │ Executes SQL │ │ JSON/XML out │
└──────────────┘ └──────────────┘ └──────────────┘
         │             │             │
         └─────────────┴─────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ Database Layer                              │
│ db_manager.py                               │
│ Connection handling & SQL execution         │
└─────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ PostgreSQL Database                         │
│ Rooms • Students • Indexes • Views          │
└─────────────────────────────────────────────┘
```

