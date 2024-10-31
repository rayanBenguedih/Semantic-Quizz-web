##
## EPITECH PROJECT, 2022
## maths
## File description:
## Makefile
##

NAME	=	quiz

all:
	chmod +x $(NAME)

clean:
	$(RM) -r __pycache__

fclean: clean

re: fclean all
