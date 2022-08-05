# Mapproxy REST Seed / cleanup endpoint plugin

`mapproxy-rest-endpoint` is a plugin for [Mapproxy (version >= 1.15)](https://mapproxy.org/) which adds a command `serve-seed-endpoint` to `mapproxy-util`.



## Examples
#### Seed and cleanup via `REST` for list of levels:

```json
{
    "seedConfig": {
        "seeds": {
            "seed1": {
                "caches": [
                    "dop_cache"
                ],
                "refresh_before": {
                    "minutes": 1
                },
                "levels": [
                    0,
                    1,
                    2
                ]
            }
        },
        "cleanups": {
            "cleanup1": {
                "caches": [
                    "dop_pan_cache"
                ],
                "levels": [
                    2
                ]
            }
        }
    },
    "config": {
        "dry_run": false,
        "concurrency": 5,
        "geom_levels": false
    }
}
```

#### Cleanup via `REST` for bounding box:
```json
{
    "seedConfig": {
        "cleanups": {
            "cleanupPolygon": {
                "caches": [
                    "dop_cache",
                    "dop_pan_cache"
                ],
                "coverages": [
                    "changes_entity_area1"
                ]
            }
        },
        "coverages": {
            "changes_entity_area1": {
                "bbox": [
                    638207.82,
                    5683208.6,
                    638666.91,
                    5683227.69
                ],
                "srs": "EPSG:25832"
            }
        }
    },
    "config": {
        "dry_run": false,
        "concurrency": 5,
        "geom_levels": false
    }
}
```
