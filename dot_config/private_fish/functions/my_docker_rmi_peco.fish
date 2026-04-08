function my_docker_rmi_peco
    set -l selected (docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | peco)
    or return 1

    set -l image_id (string split ' ' -- $selected)[-1]
    test -n "$image_id"
    or return 1

    docker rmi $image_id
end
