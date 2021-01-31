export PS1="\e[0;37m\]\u@\e[4;31m\]\h\e[0;37m\] \w \e[0m\]> "

readonly RESET='\\033[0;0m'
readonly HIGLIGHT='\\033[1;31m'

while read CMD; do
    echo -e "$CMD"
done <<EOF
${HIGLIGHT}=> HELP TO START ${RESET}

First, you probably want to update python dependencies :
> ${HIGLIGHT}pipenv install --dev${RESET}

Then you should chroot in a dedicated python env:
> ${HIGLIGHT}pipenv shell${RESET}

Then you probably want to launch api :
> ${HIGLIGHT}python serve.py${RESET}

EOF
