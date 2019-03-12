 INCLUDE Irvine32.inc
    .data
		w DWORD 40
		h DWORD 40
		map BYTE 1700 dup(2)	;2=moveable 1=snake 0=food
		snake DWORD 1600 dup(0)	;(x,y)
		snakehead DWORD 1
		snaketail DWORD 0
		dir BYTE 1	;1=up 2=down 3=left 4=right
		border BYTE "��",0
		border2 BYTE "�@",0
		head BYTE "��",0
		body BYTE "��",0
		food BYTE "��",0
		nowhead DWORD 0
		scoreMsg BYTE "Score:",0
		count DWORD 0
		speedMsg BYTE "Speed:",0
		speed DWORD 500
		dieMsg BYTE "You are die. score:",0
	.code
	xy2line PROC USES ebx	;Ū��ebx�����(x,y)�^�ǩ�eax(x+wy)
		mov eax,0
		mov al,bh	;al=y
		add al,bh	;al=2y
		mul w		;al=2wy
		mov bh,0
		add ax,bx
		shr ax,1
		ret
	xy2line ENDP

	genfood PROC	;eax=x+wy ebx=(x,y) edx="��"
	regen:
		mov eax,h
		call RandomRange	;eax = 0 ~ (h-1)
		inc eax				;eax = 1 ~ h
		mov dh,al

		mov eax,w
		call randomRange	;eax = 0 ~ (w-1)
		inc eax				;eax = 1 ~ w
		shl al,1			;eax = [2 ... w , 2]
		mov dl,al

		mov ebx,edx
		call xy2line
		mov dl,map[eax]
		cmp dl,1
	je regen
		cmp dl,0
	je regen
		mov map[eax],0
		mov edx,ebx
		call Gotoxy
		mov edx,OFFSET food
		call WriteString

		ret
	genfood ENDP

	main PROC
		;�إߦa��
		;�W���
		mov ecx,w
		add ecx,2
		upperedge:
		mov edx,OFFSET border
		call WriteString
		loop upperedge
		call Crlf
		;���k���
		mov ecx,h
		mov ebx,0
		L1:
		push ecx
		mov ecx,w
		mov edx,OFFSET border
		call WriteString
		L2:
		mov edx,OFFSET border2
		call WriteString
		loop L2
		mov edx,OFFSET border
		call WriteString
		call Crlf
		pop ecx
		loop L1
		;�U���
		mov ecx,w
		add ecx,2
		L3:
		mov edx,OFFSET border
		call WriteString
		loop L3
		call Crlf

		;��l�ơG�D�B����
		;�D�Y
			;1.���o�y��edx=(x,y)
		mov edx,0
		mov eax,w	;eax=w
		mov dl,al	;dl=w
		mov eax,h	;eax=h
		mov dh,al	;dh=h d=(h,w)
		shr dh,1	;d=(h/2,w)	�]�w�Y����m
		shr dl,1	;w���i���_��
		shl dl,1	
			;2.�N�y�Цs�J�D��queue
		mov ebx,snakehead
		mov snake[ebx*4],edx	;�D���Y
		mov nowhead,edx
			;3.��s�e��
		call Gotoxy
		mov ebx,edx
		mov edx,OFFSET head
		call WriteString		;�e�����Y
			;4.��s�a��
		call xy2line
		mov nowhead,eax
		mov map[eax],1			;�a�ϩ��Y
		;ax=x+wy bx=(x,y) dx=head

		;�D��
			;1.���o�y��edx=(x,y)
		add bh,1
		mov dx,bx	
			;2.�N�y�Цs�J�D��queue
		mov ebx,snaketail
		mov snake[ebx*4],edx
			;3.��s�e��
		call Gotoxy
		mov ebx,edx
		mov edx,OFFSET body
		call WriteString
			;4.��s�a��
		call xy2line
		mov map[eax],1
		;ax=x+wy bx=(x,y) dx=body

		;���ͭ���
		call genfood	;eax=x+wy ebx=(x,y) edx="��"

		;�}�l�C��
		islive:
		;�ˬd��L�O�_�Q���U�A�ýվ�e�i��V
		call ReadKey	;a=(key,0) b=NULL c=NULL
		mov al,ah
		mov ah,0
		cmp al,0
		jz nokey
		;�Y�Q���U�i��վ��V
			cmp al,72
			jne key2
			cmp dir,2
			je nokey
			mov dir,1
			jmp nokey

		key2:
			cmp al,80
			jne key3
			cmp dir,1
			je nokey
			mov dir,2
			jmp nokey

		key3:
			cmp al,75
			jne key4
			cmp dir,4
			je nokey
			mov dir,3
			jmp nokey

		key4:
			cmp al,77
			jne key5
			cmp dir,3
			je nokey
			mov dir,4
			jmp nokey

		key5:	;press +
			cmp al,78
			jne key6
			add speed,10
			jmp nokey

		key6:	;press -
			cmp al,74
			jne nokey
			cmp speed,50
			jb nokey
			sub speed,10
			jmp nokey

		nokey:
		;�P�_�O�_����íp��s�Y����m(x,y)��dx
		mov ebx,snakehead		;�D�Y�bqueue����m
		mov edx,snake[ebx*4]	;�D�Y�e�����u�y�Сv

		cmp dir,1		;��V���W
		jne dir2
		cmp dh,1		;dh <= 1 ?
		jbe die
		dec dh			;dh--
		mov eax,w		;eax = w
		sub nowhead,eax	;nowhead -= eax

		dir2:
		cmp dir,2		;��V���U
		jne dir3
		mov eax,h
		cmp dh,al		;dh >= h ?
		jae die
		inc dh			;dh++
		mov eax,w		;eax = w
		add nowhead,eax	;nowhead += eax

		dir3:
		cmp dir,3		;��V����
		jne dir4
		cmp dl,2		;dl <=1 ?
		jbe die
		sub dl,2		;dl -= 2
		sub nowhead,1	;nowhead --

		dir4:
		cmp dir,4		;��V���k
		jne dir5
		mov eax,w
		add eax,w
		cmp dl,al		;dh >= 2w ?
		jae die
		add dl,2		;dl +=2
		add nowhead,1	;nowhead ++

		dir5:
		mov eax,nowhead
		inc ebx			;�N�D���Ӫ��Y�[�W�h
		mov snake[ebx*4],edx
		;�P�_�O�_����ۤv
		mov ebx,0
		mov bl,map[eax]
		cmp bl,1
		je die
		;�P�_�O�_������(����ơB�W�[�����ø��L�h��)
			;�����
			cmp ebx,0
			jne deltail
			mov eax,count
			add eax,10
			mov count,eax
			;���s���ͭ���
			call genfood	;eax=x+wy ebx=(x,y) edx="��"


		jmp addhead
		;��s�e��
		deltail:		;�h�� 
			;1.���o�y��
		mov eax,snaketail		;�D���bqueue����m
		mov edx,snake[eax*4]	;�D���b�e�����y��(x,y)
			;2.�s�J�D��queue
		inc eax
		mov snaketail,eax
			;3.��s�e��
		call Gotoxy
		mov ebx,edx
		mov edx,OFFSET border2
		call WriteString	;�e���h��
			;4.��s�a��
		call xy2line
		mov map[eax],2		;�a�ϥh��

		addhead:	;�h�Y
			;1.���o�y��
		mov eax,snakehead		;�D�Y�bqueue����m
		mov edx,snake[eax*4]	;�D�Y�b�e�����y��
			;3.��s�e��
		call Gotoxy
		mov edx,OFFSET body
		call WriteString		;�e���H�����л\�Y
					;�W�Y
			;1.���o�y��
		inc eax
		mov snakehead,eax		;�D�s�Y�bqueue����m
		mov edx,snake[eax*4]
			;3.��s�e��
		call Gotoxy
		mov ebx,edx
		mov ecx,edx
		mov edx,OFFSET head
		call WriteString
			;4.��s�a��
		call xy2line
		mov map[eax],1		;�a�ϼW�Y

		;��ܤ���
		mov dh,43
		mov dl,0
		call Gotoxy
		mov edx,OFFSET scoreMsg
		call WriteString
		mov eax,count
		call WriteDec
		mov eax,'  '
		call WriteChar

		mov dh,44
		mov dl,0
		call Gotoxy
		mov edx,OFFSET speedMsg
		mov eax,0
		call WriteString
		mov eax,speed
		call WriteDec

		call Delay
		jmp islive

		die:	;���`���᪺�ʧ@
		;�^����I
		mov eax,h
		add eax,2
		mov dl,0
		mov dh,al
		call Gotoxy
		mov edx,OFFSET dieMsg
		call WriteString
		mov eax,count
		call WriteDec
		call Crlf
	call WaitMsg ; �Ȱ�
    exit
    main ENDP
    END main