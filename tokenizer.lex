%{
#include <stdio.h>
#include <stdlib.h>
int line_number = 1;
int column_number = 1;
#define YY_USER_ACTION column_number += yyleng;
%}

%option noyywrap

KEYWORD       (if|then|else|fi|for|while|do|done|echo|exit|case|esac|select|until|declare|typeset|local|export|readonly|shift|getopts|let|test|time|trap|umask|unset|eval|exec|wait|read|printf|source|alias|unalias|type|set|help|history|true|false|function|return|break|continue)
DELIMITER     [\(\)\{\}\[\];,]
STRING_LITERAL \"[^\"]*\"
NUMBER        [0-9]+
IDENTIFIER    [_a-zA-Z][_a-zA-Z0-9]*

VARIABLE      \$[_a-zA-Z][_a-zA-Z0-9]*|\$[0-9]+|\$\{[^}]+\}|\$\{?[_a-zA-Z][_a-zA-Z0-9]*\}?

OPTION        -{1,2}[a-zA-Z]+

WORD          [a-zA-Z0-9_/.-]+

WHITESPACE    [ \t]+
NEWLINE       \n
COMMENT       \#.*

%%

{NEWLINE}           { printf("[Line %d, Column %d] NEWLINE: %s\n", line_number, column_number, yytext); line_number++; column_number = 1; }
{WHITESPACE}        { printf("[Line %d, Column %d] WHITESPACE: %s\n", line_number, column_number, yytext); column_number += yyleng; }

"cd"                { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"ls"                { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"pacman"            { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"sudo"              { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"rm"                { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"cp"                { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"mv"                { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"echo"              { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"cat"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"chmod"             { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"chown"             { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"makepkg"           { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"tar"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"find"              { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"grep"              { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"awk"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"sed"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"systemctl"         { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"journalctl"        { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"mkfs"              { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"lsblk"             { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"mount"             { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"umount"            { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"nano"              { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"vim"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"man"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"ps"                { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }
"top"               { printf("[Line %d, Column %d] COMMAND: %s\n", line_number, column_number, yytext); }

"&&"                { printf("[Line %d, Column %d] AND: %s\n", line_number, column_number, yytext); }
"||"                { printf("[Line %d, Column %d] OR: %s\n", line_number, column_number, yytext); }
"=="                { printf("[Line %d, Column %d] EQUALS: %s\n", line_number, column_number, yytext); }
"!="                { printf("[Line %d, Column %d] NOT_EQUALS: %s\n", line_number, column_number, yytext); }
"<="                { printf("[Line %d, Column %d] LESS_OR_EQUAL: %s\n", line_number, column_number, yytext); }
">="                { printf("[Line %d, Column %d] GREATER_OR_EQUAL: %s\n", line_number, column_number, yytext); }
"+"                 { printf("[Line %d, Column %d] PLUS: %s\n", line_number, column_number, yytext); }
"-"                 { printf("[Line %d, Column %d] MINUS: %s\n", line_number, column_number, yytext); }
"*"                 { printf("[Line %d, Column %d] MULTIPLY: %s\n", line_number, column_number, yytext); }
"/"                 { printf("[Line %d, Column %d] DIVIDE: %s\n", line_number, column_number, yytext); }
"="                 { printf("[Line %d, Column %d] ASSIGN: %s\n", line_number, column_number, yytext); }
"<"                 { printf("[Line %d, Column %d] LESS_THAN: %s\n", line_number, column_number, yytext); }
">"                 { printf("[Line %d, Column %d] GREATER_THAN: %s\n", line_number, column_number, yytext); }
"!"                 { printf("[Line %d, Column %d] NOT: %s\n", line_number, column_number, yytext); }
":"                 { printf("[Line %d, Column %d] COLON: %s\n", line_number, column_number, yytext); }
";"                 { printf("[Line %d, Column %d] SEPARATOR: %s\n", line_number, column_number, yytext); }
"|"                 { printf("[Line %d, Column %d] PIPE: %s\n", line_number, column_number, yytext); }
">>"                { printf("[Line %d, Column %d] APPEND_REDIRECT: %s\n", line_number, column_number, yytext); }

{COMMENT}           { printf("[Line %d, Column %d] COMMENT: %s\n", line_number, column_number, yytext); }
{KEYWORD}           { printf("[Line %d, Column %d] KEYWORD: %s\n", line_number, column_number, yytext); }
{DELIMITER}         { printf("[Line %d, Column %d] DELIMITER: %s\n", line_number, column_number, yytext); }
{STRING_LITERAL}    { printf("[Line %d, Column %d] STRING_LITERAL: %s\n", line_number, column_number, yytext); }
{OPTION}            { printf("[Line %d, Column %d] OPTION: %s\n", line_number, column_number, yytext); }
{NUMBER}            { printf("[Line %d, Column %d] NUMBER: %s\n", line_number, column_number, yytext); }
{IDENTIFIER}        { printf("[Line %d, Column %d] IDENTIFIER: %s\n", line_number, column_number, yytext); }
{VARIABLE}          { printf("[Line %d, Column %d] VARIABLE: %s\n", line_number, column_number, yytext); }
{WORD}              { printf("[Line %d, Column %d] ARGUMENT: %s\n", line_number, column_number, yytext); }

.                   { printf("[Line %d, Column %d] ERROR: %s\n", line_number, column_number, yytext); }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            fprintf(stderr, "Cannot open %s\n", argv[1]);
            exit(1);
        }
    }
    printf("Starting Bash Command Parser\n");
    printf("----------------------------\n");
    yylex();
    printf("----------------------------\n");
    printf("Parsing Complete - Processed %d lines\n", line_number);
    return 0;
}