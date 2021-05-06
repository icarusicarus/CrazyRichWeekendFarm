# k-scheme README

<img src="https://github.com/icaruswithoutwings/CrazyRichWeekendFarm/blob/main/Images/welcome.png">


This is a Korean Scheme Interpreter and the VSCode Extension that provides it.

It gives you to scheme programming in Korean.

Interpreter is provided in two way usages. You can type `kscheme` and use this as an Interpreter. If you want to interpreting the file, you can type `kschme [filename]` .

VSCode Extension support snippet and syntax highlighting.(But It needs to be revised.)





## Korean Keyword



| English   | Korean    |
|:---------:|:---------:|
| define    | 정의      |
| lambda    | 람다      |
| if        | 만약      |
| quote     | 쿼트      |
| cons      | 쌍쌍      |
| car       | 머리      |
| cdr       | 꼬리      |





## How to Run


1. Search **k-scheme** at VSCode Marketplace and Install it.
2. Clone this project

    ```
    git clone https://github.com/icaruswithoutwings/CrazyRichWeekendFarm.git
    ````

3. Add 'dist' directory path to environmental variable. It makes the **kscheme.exe** file, a Korean Scheme Interpreter, available evertywhere.
4. Add this code to the tasks.json file.

    ```json
    {
    	"version": "2.0.0",
    	"tasks": [
    		{
    			"type": "shell",
    			"label": "kscheme.exe build active file",
    			"command": "kscheme.exe",
    			"args": [
    				"${file}"
    			],
    			"group": {
    				"kind": "build",
    				"isDefault": true
    			}
    		}
    	]
    }
    ```

5. Run the Test set. (Ctrl + Shift + B)





## Simple Demo



```scheme
(정의 다람쥐 (람다 (가) (+ 가 가)))
(다람쥐 10)
;... 다람쥐 귀여워
(정의 숫자 15)
(다람쥐 15)
(정의 팩토리얼 (람다 (가) (만약 (= 가 0) 1 (* 가 (팩토리얼 (- 가 1))))))
(팩토리얼 숫자)
```





## Usage



- Interpreter

<img src="https://github.com/icaruswithoutwings/CrazyRichWeekendFarm/blob/main/Images/usage1.gif">


- Using file input

<img src="https://github.com/icaruswithoutwings/CrazyRichWeekendFarm/blob/main/Images/usage2.gif">





## Lisence



- [MIT](http://opensource.org/licenses/MIT)