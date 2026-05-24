.MODEL SMALL
.STACK 100H

.DATA
msg_prompt     DB 13, 10, 'Enter option (A=Arm, D=Disarm, 1=PIR, 2=Door, 3=Panic, ESC=Exit): $'
armed_msg      DB 13, 10, 'System Armed (LED ON)$'
disarmed_msg   DB 13, 10, 'System Disarmed (LED OFF)$'
alarm_msg      DB 13, 10, 'ALARM TRIGGERED! (Buzzer ON)$'
buzzer_prompt  DB 13, 10, 'Press B to turn off buzzer, any other key to keep it ON: $'
buzzer_off_msg DB 13, 10, 'Buzzer turned OFF by user.$'

system_armed   DB 0
alarm_active   DB 0

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

START:
    ; Show prompt
    LEA DX, msg_prompt
    MOV AH, 09H
    INT 21H

    ; Wait for user input
    MOV AH, 01H
    INT 21H
    MOV BL, AL ; store key in BL

    ; Handle key
    CMP BL, 1BH     ; ESC
    JE EXIT_PROGRAM
    CMP BL, 'A'
    JE ARM_SYSTEM
    CMP BL, 'a'
    JE ARM_SYSTEM
    CMP BL, 'D'
    JE DISARM_SYSTEM
    CMP BL, 'd'
    JE DISARM_SYSTEM
    CMP BL, '1'
    JE TRIGGER_PIR
    CMP BL, '2'
    JE TRIGGER_DOOR
    CMP BL, '3'
    JE TRIGGER_PANIC

    JMP START

; ---- ARMING SYSTEM ----
ARM_SYSTEM:
    MOV system_armed, 1
    MOV AL, 00000001B ; LED ON
    OUT 199, AL
    LEA DX, armed_msg
    MOV AH, 09H
    INT 21H
    JMP START

; ---- DISARMING SYSTEM ----
DISARM_SYSTEM:
    MOV system_armed, 0
    MOV alarm_active, 0
    MOV AL, 00000000B ; LED OFF
    OUT 199, AL
    LEA DX, disarmed_msg
    MOV AH, 09H
    INT 21H
    JMP START

; ---- SENSORS ----
TRIGGER_PIR:
    CMP system_armed, 1
    JNE START
    JMP TRIGGER_ALARM

TRIGGER_DOOR:
    CMP system_armed, 1
    JNE START
    JMP TRIGGER_ALARM

TRIGGER_PANIC:
    ; Panic triggers even if system is disarmed
    JMP TRIGGER_ALARM

; ---- ALARM ----
TRIGGER_ALARM:
    MOV alarm_active, 1
    MOV AL, 00000011B ; LED + Buzzer ON
    OUT 199, AL
    LEA DX, alarm_msg
    MOV AH, 09H
    INT 21H

    ; Ask user to disable buzzer
    LEA DX, buzzer_prompt
    MOV AH, 09H
    INT 21H

    ; Wait for input
    MOV AH, 01H
    INT 21H
    CMP AL, 'B'
    JE TURN_OFF_BUZZER

    ; Keep buzzer ON for 3 seconds
    MOV CX, 3
DELAY_LOOP:
    PUSH CX
    CALL DELAY_1SEC
    POP CX
    LOOP DELAY_LOOP
    JMP RESET_ALARM

TURN_OFF_BUZZER:
    ; Show message
    LEA DX, buzzer_off_msg
    MOV AH, 09H
    INT 21H

    ; LED ON only
    MOV AL, 00000001B
    OUT 199, AL
    JMP START

RESET_ALARM:
    ; Reset alarm
    MOV alarm_active, 0
    CMP system_armed, 1
    JE LED_ON
    MOV AL, 00000000B ; OFF
    JMP SHOW_FINAL
LED_ON:
    MOV AL, 00000001B ; LED ON
SHOW_FINAL:
    OUT 199, AL
    JMP START

; ---- 1-SECOND DELAY ----
DELAY_1SEC PROC
    PUSH CX
    MOV CX, 0FFFFH
D1:
    LOOP D1
    POP CX
    RET
DELAY_1SEC ENDP

; ---- EXIT ----
EXIT_PROGRAM:
    MOV AH, 4CH
    INT 21H

END MAIN
