function my_cdls
    builtin cd $argv
    or return 1

    ls
end
