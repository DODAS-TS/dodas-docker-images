## How to use

Example withing a docker compose service:

```yaml
version: "3.9"

services:
    [...]
    
    backup_service:
        image: dodasts/backup-service
        volumes:
        - /path/of/source/folder:/source
        - /path/of/backup/folder:/var/cache/rsnapshot

    [...]
```