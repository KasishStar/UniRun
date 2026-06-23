_unirun_completions() {
    local cur prev words cword
    _init_completion || return

    local commands="help version doctor history search install run config"

    if [[ $cword -eq 1 ]]; then
        COMPREPLY=($(compgen -W "$commands" -- "$cur"))
    elif [[ $cword -eq 2 ]]; then
        case "${words[1]}" in
            run|search|install)
                COMPREPLY=($(compgen -f -- "$cur"))
                ;;
        esac
    fi
}

complete -F _unirun_completions unirun
