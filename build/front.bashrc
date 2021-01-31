export PS1="\e[0;37m\]\u@\e[4;32m\]\h\e[0;37m\] \w \e[0m\]> "

readonly RESET='\\033[0;0m'
readonly HIGLIGHT='\\033[1;32m'

while read CMD; do
    echo -e "$CMD"
done <<EOF
${HIGLIGHT}=> HELP TO START ${RESET}

First, you probably want to update npm dependencies :
> ${HIGLIGHT}npm install${RESET}

Then you probably want to launch front server :
> ${HIGLIGHT}npm run serve${RESET}

EOF
