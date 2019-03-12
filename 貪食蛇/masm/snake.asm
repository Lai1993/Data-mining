 INCLUDE Irvine32.inc
    .data
		w DWORD 40
		h DWORD 40
		map BYTE 1700 dup(2)	;2=moveable 1=snake 0=food
		snake DWORD 1600 dup(0)	;(x,y)
		snakehead DWORD 1
		snaketail DWORD 0
		dir BYTE 1	;1=up 2=down 3=left 4=right
		border BYTE "Ｘ",0
		border2 BYTE "　",0
		head BYTE "Ｈ",0
		body BYTE "Ｂ",0
		food BYTE "Ｆ",0
		nowhead DWORD 0
		scoreMsg BYTE "Score:",0
		count DWORD 0
		speedMsg BYTE "Speed:",0
		speed DWORD 500
		dieMsg BYTE "You are die. score:",0
	.code
	xy2line PROC USES ebx	;讀取ebx的資料(x,y)回傳於eax(x+wy)
		mov eax,0
		mov al,bh	;al=y
		add al,bh	;al=2y
		mul w		;al=2wy
		mov bh,0
		add ax,bx
		shr ax,1
		ret
	xy2line ENDP

	genfood PROC	;eax=x+wy ebx=(x,y) edx="Ｆ"
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
		;建立地圖
		;上邊界
		mov ecx,w
		add ecx,2
		upperedge:
		mov edx,OFFSET border
		call WriteString
		loop upperedge
		call Crlf
		;左右邊界
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
		;下邊界
		mov ecx,w
		add ecx,2
		L3:
		mov edx,OFFSET border
		call WriteString
		loop L3
		call Crlf

		;初始化：蛇、食物
		;蛇頭
			;1.取得座標edx=(x,y)
		mov edx,0
		mov eax,w	;eax=w
		mov dl,al	;dl=w
		mov eax,h	;eax=h
		mov dh,al	;dh=h d=(h,w)
		shr dh,1	;d=(h/2,w)	設定頭的位置
		shr dl,1	;w不可為奇數
		shl dl,1	
			;2.將座標存入蛇的queue
		mov ebx,snakehead
		mov snake[ebx*4],edx	;蛇放頭
		mov nowhead,edx
			;3.刷新畫面
		call Gotoxy
		mov ebx,edx
		mov edx,OFFSET head
		call WriteString		;畫面放頭
			;4.刷新地圖
		call xy2line
		mov nowhead,eax
		mov map[eax],1			;地圖放頭
		;ax=x+wy bx=(x,y) dx=head

		;蛇身
			;1.取得座標edx=(x,y)
		add bh,1
		mov dx,bx	
			;2.將座標存入蛇的queue
		mov ebx,snaketail
		mov snake[ebx*4],edx
			;3.刷新畫面
		call Gotoxy
		mov ebx,edx
		mov edx,OFFSET body
		call WriteString
			;4.刷新地圖
		call xy2line
		mov map[eax],1
		;ax=x+wy bx=(x,y) dx=body

		;產生食物
		call genfood	;eax=x+wy ebx=(x,y) edx="Ｆ"

		;開始遊戲
		islive:
		;檢查鍵盤是否被按下，並調整前進方向
		call ReadKey	;a=(key,0) b=NULL c=NULL
		mov al,ah
		mov ah,0
		cmp al,0
		jz nokey
		;若被按下進行調整方向
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
		;判斷是否撞牆並計算新頭的位置(x,y)於dx
		mov ebx,snakehead		;蛇頭在queue的位置
		mov edx,snake[ebx*4]	;蛇頭畫面的「座標」

		cmp dir,1		;方向為上
		jne dir2
		cmp dh,1		;dh <= 1 ?
		jbe die
		dec dh			;dh--
		mov eax,w		;eax = w
		sub nowhead,eax	;nowhead -= eax

		dir2:
		cmp dir,2		;方向為下
		jne dir3
		mov eax,h
		cmp dh,al		;dh >= h ?
		jae die
		inc dh			;dh++
		mov eax,w		;eax = w
		add nowhead,eax	;nowhead += eax

		dir3:
		cmp dir,3		;方向為左
		jne dir4
		cmp dl,2		;dl <=1 ?
		jbe die
		sub dl,2		;dl -= 2
		sub nowhead,1	;nowhead --

		dir4:
		cmp dir,4		;方向為右
		jne dir5
		mov eax,w
		add eax,w
		cmp dl,al		;dh >= 2w ?
		jae die
		add dl,2		;dl +=2
		add nowhead,1	;nowhead ++

		dir5:
		mov eax,nowhead
		inc ebx			;將蛇未來的頭加上去
		mov snake[ebx*4],edx
		;判斷是否撞到自己
		mov ebx,0
		mov bl,map[eax]
		cmp bl,1
		je die
		;判斷是否有食物(算分數、增加食物並跳過去尾)
			;算分數
			cmp ebx,0
			jne deltail
			mov eax,count
			add eax,10
			mov count,eax
			;重新產生食物
			call genfood	;eax=x+wy ebx=(x,y) edx="Ｆ"


		jmp addhead
		;刷新畫面
		deltail:		;去尾 
			;1.取得座標
		mov eax,snaketail		;蛇尾在queue的位置
		mov edx,snake[eax*4]	;蛇尾在畫面的座標(x,y)
			;2.存入蛇的queue
		inc eax
		mov snaketail,eax
			;3.刷新畫面
		call Gotoxy
		mov ebx,edx
		mov edx,OFFSET border2
		call WriteString	;畫面去尾
			;4.刷新地圖
		call xy2line
		mov map[eax],2		;地圖去尾

		addhead:	;去頭
			;1.取得座標
		mov eax,snakehead		;蛇頭在queue的位置
		mov edx,snake[eax*4]	;蛇頭在畫面的座標
			;3.刷新畫面
		call Gotoxy
		mov edx,OFFSET body
		call WriteString		;畫面以身體覆蓋頭
					;增頭
			;1.取得座標
		inc eax
		mov snakehead,eax		;蛇新頭在queue的位置
		mov edx,snake[eax*4]
			;3.刷新畫面
		call Gotoxy
		mov ebx,edx
		mov ecx,edx
		mov edx,OFFSET head
		call WriteString
			;4.刷新地圖
		call xy2line
		mov map[eax],1		;地圖增頭

		;顯示分數
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

		die:	;死亡之後的動作
		;回到原點
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
	call WaitMsg ; 暫停
    exit
    main ENDP
    END main