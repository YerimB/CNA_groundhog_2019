##
## EPITECH PROJECT, 2020
## CNA_groundhog_2019
## File description:
## Makefile
##

NAME	=	groundhog

all:
	cp groundhog.py $(NAME)

clean:
	rm -rf $(NAME)

fclean: clean

re:	clean all