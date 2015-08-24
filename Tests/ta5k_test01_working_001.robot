*** Settings ***
Documentation  This is some basic info about the whole suite
Library  Telnet
Library  cnpq_general

*** Variables ***
${ip}  10.213.253.30
${ip_list}  '10.213.253.30 10.13.100.81 10.213.253.35 10.213.253.38'
${aucFileName}  C:\\Users\\teggenbe800w7\\Desktop\\TA5000-0900000030.auc
${usr}  ADMIN
${pwd}  PASSWORD
${cmd}  show table int vdsl

*** Test Cases ***
User must sign in to check out
    [Documentation]  Perform AUC, login to a SUT and perform a command
    #AUC CHECKER
    #Auc Checker  ${ip_list}  ${aucFileName}
    #OPEN SHELF AND PERFORM COMMAND
    Open Connection  ${ip}  port=23
    Login  ADMIN  PASSWORD  login_prompt=Username:  password_prompt=Password:
    Set Prompt  > |#  prompt_is_regexp=true
    Write  enable
    Read Until Prompt
    Write  term len 0
    Read Until Prompt
    Write  ${cmd}
    Read Until Prompt
    Close Connection



