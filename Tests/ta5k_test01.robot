*** Settings ***
Documentation     This is some basic info about the whole suite
Library           Telnet
Library           cnpq_general.py

*** Variables ***
${ip}             10.13.65.101
${ip_list}        '10.13.65.101 110.13.65.116 10.13.65.117 10.13.65.118'
${aucFileName}    C:\\Users\\teggenbe800w7\\Desktop\\TA5000-0900000030.auc
${usr}            ADMIN
${pwd}            PASSWORD
${cmd}            show table int vdsl
${time_stamp}     dog

*** Test Cases ***
simple_test
    [Documentation]    Simple test that runs AUC check and logs in SUT to perform a command ${cmd}
    Auc Checker    10.13.65.101    TA5000-0900000030.auc
    Open Connection    ${ip}    port=23
    Login    ADMIN    PASSWORD    login_prompt=Username:    password_prompt=Password:
    Set Prompt    > |#    prompt_is_regexp=true
    Write    enable
    Read Until Prompt
    Write    term len 0
    Read Until Prompt
    Write    ${cmd}
    Read Until Prompt
    Close Connection
