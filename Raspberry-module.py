
while(1):
    import RPi.GPIO as GPIO
    import time
    import math
    from espeak import espeak
    import os
    import serial
    #GPIO to LCD mapping
    LCD_RS = 26
    LCD_E  = 24
    LCD_D4 = 22
    LCD_D5 = 18
    LCD_D6 = 16
    LCD_D7 = 12
    # Display constants
    LCD_WIDTH = 16  # Maximum characters per line
    LCD_CHR = True
    LCD_CMD = False

    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005

    def main():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LCD_E, GPIO.OUT)  # E
        GPIO.setup(LCD_RS, GPIO.OUT)  # RS
        GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
        GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
        GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
        GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
	
    def lcd_init():
        # Initialise display
        lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        time.sleep(E_DELAY)


    def lcd_byte(bits, mode):
		
        GPIO.output(LCD_RS, mode)  # RS
        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits& 0x10== 0x10:
            GPIO.output(LCD_D4, True)
        if bits& 0x20== 0x20 :
            GPIO.output(LCD_D5, True)
        if bits& 0x40 == 0x40 :
            GPIO.output(LCD_D6, True)
        if bits& 0x80 == 0x80 :
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        lcd_toggle_enable()

        # Low bits
        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits& 0x01 == 0x01 :

            GPIO.output(LCD_D4, True)
        if bits& 0x02 == 0x02 :
            GPIO.output(LCD_D5, True)
        if bits& 0x04 == 0x04 :
            GPIO.output(LCD_D6, True)
        if bits& 0x08 == 0x08 :
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        lcd_toggle_enable()

    def lcd_toggle_enable():
        # Toggle enable
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)

    def lcd_string(message, line):
        # Send string to display
        message = message.ljust(LCD_WIDTH," " )
        lcd_byte(line, LCD_CMD)
        for i in range(LCD_WIDTH):
            lcd_byte(ord(message[i]), LCD_CHR)

    if __name__ == '__main__':

        try:
            main()
        except KeyboardInterrupt:
            pass
        finally:
            lcd_byte(0x01, LCD_CMD)
            lcd_string("Goodbye!", LCD_LINE_1)
            GPIO.cleanup()

    GPIO.setmode (GPIO.BOARD)

    MATRIX = [ [1, 2, 3, 'A'],
              [4, 5, 6, 'B'],
              [7, 8, 9, 'C'],
              ['*', 0, '#', 'D']]

    ROW = [29, 31, 33, 35]
    COL = [37, 38, 40, 36]

    main()
    lcd_init()
    lcd_string("ENTER AMOUNT", LCD_LINE_1)
    lcd_string("---------------------", LCD_LINE_2)

    time.sleep(3)  # 3 second delay

    for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], 1)

    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    k = 0
    sum = 0
    while(input!='D' or sum==0):
       	for j in range (4):
       		GPIO.output(COL[j],0)
       	 	for i in range(4):
               		if GPIO.input (ROW[i]) == 0:
	                    print MATRIX[i][j]
               		    input=MATRIX[i][j]
                   
	                    if(input=='B'):
               		        sum=sum/10
                       		say2=str(sum)
	                        lcd_string(say2,LCD_LINE_2)
               		    if input>=0 and input<=9:
	                        sum = sum*10 + input                
               		        k=k+1
	                        say2=str(sum)
               		        lcd_string(say2,LCD_LINE_2)
	                    time.sleep(1)
               		    while (GPIO.input(ROW[i]) == 0):
	                        pass
       		GPIO.output(COL[j],1)
    AMOUNT=sum
	
    say = "Rs." + str(AMOUNT)
    lcd_string(say, LCD_LINE_1)
    lcd_string("TAP RFID CARD", LCD_LINE_2)

    say = "espeak '" + str(AMOUNT)+" Roopees'  2>/dev/null"
    os.system(say)
    say="espeak 'Please Tap Your R F I D Card' 2>/dev/null"
    os.system(say)


    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

    while True:
        string = ser.read(18)

        if len(string) != 0:
            string = string[1:11]  # Strip header/trailer
            print string
            break

    lcd_string("Processing", LCD_LINE_1)
    lcd_string(" ", LCD_LINE_2)
    #say='espeak "Processing" 2>/dev/null'
    #os.system(say)
    for i in range (4):
	dots="."*i
        lcd_string(dots, LCD_LINE_2)
	time.sleep(0.5)

#    say='espeak  "Please Wait"   2>/dev/null'
 #   os.system(say)

    cust_rfid = string
    
    import mysql.connector
    from mysql.connector import errorcode
#      lcd_string("TAP RFID CARD", LCD_LINE_1)
    # Obtain connection string information from the portal
    config = {
        'host': '',
        'user': '',
        'password': '',
        'database': ''
    }
    try:
        conn = mysql.connector.connect(**config)
	print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM iitjstud where tag="%s"' % (cust_rfid))
        result = cursor.fetchall()
        print result[0]
        say = "Hello " + result[0][2]
        lcd_string(say, LCD_LINE_1)
        say='espeak  Hello   2>/dev/null'
        os.system(say)
        say="espeak " +result[0][2]+ " 2>/dev/null"
        os.system(say)

        print result[0][6]            
	if result[0][6]<AMOUNT:
            say1 = "INSUFFICIENT BALANCE"
            lcd_string(say1, LCD_LINE_2)	    
	    #say="espeak Insufficient 2>/dev/null"
	    #os.system(say)
	    #say="espeak 'low Balance' 2>/dev/null"
            #os.system(say)
	    print say1
        else:
            cursor.execute('UPDATE iitjstud SET amount ="%s"  WHERE tag="%s" ' % (result[0][6] - AMOUNT, cust_rfid))
            cursor.execute('UPDATE seller SET amount =amount+"%s"  WHERE service_id="%s" ' % (AMOUNT, service_id))
	    #cursor.execute("INSERT INTO transactions (`amount`, `from_id/tag`, `from`, `to`, `to_id/tag`) VALUES ('%s', '%s', '%s', '%s`', '%s');"%(AMOUNT,cust_rfid,result[0][2],service_name,service_id))

            say1 = "Payment Successful"        
            lcd_string(say1, LCD_LINE_2)
	   
       	    print say1
#            say="espeak 'Payment' 2>/dev/null"
#	    os.system(say)
#	    say='espeak done 2>/dev/null'
	    say='espeak  Hello   2>/dev/null'
            os.system(say)
	    say2="'Payment Successful'"
            say="espeak " +say2 + " 2>/dev/null"
            os.system(say)
	    #os.system('espeak "done" 2>/dev/null')
            # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
    time.sleep(4)

