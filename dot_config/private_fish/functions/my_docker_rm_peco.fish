function my_docker_rm_peco
    set -l selected (docker ps -a --format '{{.Names}} {{.ID}}' | peco)
    or return 1

    set -l container_id (string split ' ' -- $selected)[-1]
    test -n "$container_id"
    or return 1

    docker rm -f $container_id
end