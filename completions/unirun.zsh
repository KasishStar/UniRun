#compdef unirun

_unirun() {
    local -a commands
    commands=(
        'help:Show help'
        'version:Show version'
        'doctor:Check system runtime status'
        'history:Show execution history'
        'search:Search for files'
        'install:Install a runtime/package'
        'run:Run a file'
        'config:Show configuration'
    )

    _arguments \
        '1:command:->commands' \
        '*:file:_files'

    case "$state" in
        commands)
            _describe -t commands 'unirun commands' commands
            ;;
    esac
}

_unirun "$@"
