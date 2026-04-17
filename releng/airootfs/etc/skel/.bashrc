#
# ~/.bashrc
#

# If not running interactively, don't do anything
if [[ $- == *i* ]]; then
    fastfetch
fi

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '
