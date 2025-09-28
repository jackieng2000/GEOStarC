

# Path to your Oh My Zsh installation.
# ---------------------------------------------------
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time Oh My Zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
# ZSH_THEME="robbyrussell"
# ----------------------------------------------------
export TERM="xterm-256color"

ZSH_THEME="powerlevel9k/powerlevel9k"

POWERLEVEL9K_PYENV_PROMPT_ALWAYS_SHOW=true
POWERLEVEL9K_GIT_STATUS_SHOW=true
POWERLEVEL9K_EXECUTION_TIME_SHOW=true
HIST_STAMPS="mm/dd/yyyy"

plugins=(git zsh-autosuggestions zsh-syntax-highlighting nvm virtualenv pyenv vscode)

POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(dir vcs pyenv virtualenv php_version nvm java_version rust_version rbenv laravel_version)

# COLOR SETTINGS 

# Production Setting   for effective source ~/.zshrc 
# POWERLEVEL9K_DIR_HOME_BACKGROUND='196'
# POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND='196'
# POWERLEVEL9K_DIR_HOME_FOREGROUND='255'
# POWERLEVEL9K_DIR_HOME_SUBFOLDER_FOREGROUND='255'

# Development Setting
POWERLEVEL9K_DIR_HOME_BACKGROUND='153'
POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND='153'
POWERLEVEL9K_DIR_HOME_FOREGROUND='0'
POWERLEVEL9K_DIR_HOME_SUBFOLDER_FOREGROUND='0'

# Both
POWERLEVEL9K_PYENV_BACKGROUND='229'
POWERLEVEL9K_VIRTUALENV_BACKGROUND='154'
POWERLEVEL9K_NVM_BACKGROUND='046'

POWERLEVEL9K_PYTHON_ICON='\UE73C'
POWERLEVEL9K_NODE_ICON="\UE718"
POWERLEVEL9K_RUST_ICON="\UE7A8"
POWERLEVEL9K_MODE='nerdfont-complete'

POWERLEVEL9K_TIME_BACKGROUND='153'
POWERLEVEL9K_TIME_FOREGROUND='0'

# POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status time command_execution_time)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status)


# prompt_virtualenv() {
#     local virtualenv_path = "$VIRTUAL_ENV"
#     if [[-n "$virtualenv_path" &&
#     "$VIRTUAL_ENV_DISABLE_PROMPT" != true ]]; then
#     "$1_prompt_segment" "$0" "$2" "green" "black" "$
#     (basename "$virtualenv_path")" 'PYTHON_ICON'
#     fi
# }



# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"




export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV='true'
export WORKON_HOME=$HOME/.virtualenvs

source $ZSH/oh-my-zsh.sh

pyenv virtualenvwrapper_lazy
