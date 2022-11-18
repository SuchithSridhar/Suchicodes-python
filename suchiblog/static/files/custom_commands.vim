set relativenumber
set textwidth=70
set tabstop=4
set shiftwidth=4
set expandtab
set clipboard=unnamedplus
set cursorline
set linebreak
set nohlsearch
set notimeout
set so=999
set updatetime=2000
set spell spelllang=en_us

colorscheme suchi-monokai
colorscheme onehalfdark
let g:airline_theme='onedark'
hi Normal guibg=NONE ctermbg=NONE
" let g:airline_theme='onehalfdark'

" Use True Colors
if exists('+termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

let g:mapleader = "\<Space>"
let g:maplocalleader = ','
" let g:auto_save = 1  " enable AutoSave on Vim startup
" let g:auto_save_write_all_buffers = 1  " write all open buffers as if you would use :wa
" let g:auto_save_events = ["InsertLeave", "TextChanged", "CursorHold", "CursorHoldI"]
let g:NERDTreeQuitOnOpen = 1
let g:NERDTreeAutoDeleteBuffer = 1
let g:NERDTreeMinimalUI = 1
let g:NERDTreeDirArrows = 1
let g:NERDTreeGitStatusConcealBrackets = 1 " default: 0

nnoremap <F5> :setlocal spell! spelllang=en_us<CR>
nnoremap <F6> 1z=
nnoremap <F7> ]s
inoremap <F5> <Esc>:setlocal spell! spelllang=en_us<CR>
inoremap <F6> <Esc>1z=

nnoremap <leader>ev :e ~/.config/nvim/custom_commands.vim<CR>
nnoremap <leader>sv :source ~/.config/nvim/custom_commands.vim<bar> :doautocmd BufRead<CR>

nnoremap <leader>ei :e ~/.config/i3/config<CR>
nnoremap <leader>ep :e ~/.config/polybar/config<CR>

imap <C-h> <Esc>:bprev<CR>
imap <C-l> <Esc>:bnext<CR>
nnoremap <C-h> :bprev<CR>
nnoremap <C-l> :bnext<CR>

nnoremap <C-j> gj
nnoremap <C-k> gk

nnoremap <C-Tab> :tabn<CR>
nnoremap <C-S-Tab> :tabp<CR>
inoremap <Esc><C-Tab> :tabn<CR>
inoremap <Esc><C-S-Tab> :tabp<CR>

inoremap jk <Esc>

nnoremap <leader>d "_d
vnoremap <leader>d "_d

autocmd FileType java inoremap <F12> System.out.println();<Left><left>
autocmd FileType markdown inoremap <F12> ![](./pic/pic.png)<Left><Left><Left><Left><Left>

autocmd BufNew,BufEnter *.md execute "silent! CocEnable"
autocmd BufLeave *.md execute "silent! CocDisable"

autocmd BufNew,BufRead *polybar/config execute "silent! set ft=dosini"

nmap <C-N> :NERDTreeToggle<CR>
nnoremap <silent> <Leader>nf :NERDTreeFind<CR>

nnoremap <leader>la <Plug>(coc-codeaction)
nnoremap <leader>ld <Plug>(coc-definition)
nnoremap <leader>le <Plug>(coc-references)
nnoremap <leader>lt <Plug>(coc-type-definition)
nnoremap <leader>ly <Plug>(coc-refactor) nnoremap <leader>lr <Plug>(coc-rename)
nnoremap <leader>lc <Plug>(coc-declaration)
nnoremap <leader>li <Plug>(coc-implementation)
nnoremap <leader>lf <Plug>(coc-format)
nnoremap <leader>lx <Plug>(coc-fix-current)
nnoremap <leader>ll <Plug>(coc-codelens-action)
nnoremap <leader>lo <Plug>(coc-diagnostic-next)
nnoremap <leader>lp <Plug>(coc-diagnostic-next-error)

nnoremap gn :bn<cr>
nnoremap gp :bp<cr>
nnoremap gd :bd<cr>  

" Use <C-l> for trigger snippet expand.
imap <C-l> <Plug>(coc-snippets-expand)

" Use <C-j> for select text for visual placeholder of snippet.
vmap <C-j> <Plug>(coc-snippets-select)

" Use <C-j> for jump to next placeholder, it's default of coc.nvim
let g:coc_snippet_next = '<c-j>'

" Use <C-k> for jump to previous placeholder, it's default of coc.nvim
let g:coc_snippet_prev = '<c-k>'

" Use <C-j> for both expand and jump (make expand higher priority.)
imap <C-j> <Plug>(coc-snippets-expand-jump)

" Use <leader>x for convert visual selected code to snippet
xmap <leader>x  <Plug>(coc-convert-snippet)

" Custom commands

:command SpellcheckOn :set spell spelllang=en_us
:command SpellcheckOff :set nospell

:command Tab2 :set shiftwidth=2
:command Tab4 :set shiftwidth=4

:command Javabase read $HOME/Programming/Java/snippets/base.java
:command Cbase read $HOME/Programming/snippets/C/base.c
:command HTMLbase read $HOME/Programming/HTML-CSS/snippets/base.html
:command CS1073base read $HOME/Programming/HTML-CSS/snippets/cs1073.html
:command CS1083base read $HOME/Programming/HTML-CSS/snippets/cs1083.html
:command CS1203base read $HOME/Programming/HTML-CSS/snippets/cs1203.html

:command AddBootstrap5CSS read $HOME/Programming/snippets/bootstrap/bootstrap5-css.html
:command AddBootstrap5JS read $HOME/Programming/snippets/bootstrap/bootstrap5-js.html
:command AddJquery read $HOME/Programming/snippets/javascript/jquery.html

command! -nargs=0 Prettier :CocCommand prettier.formatFile

call plug#begin('~/.local/share/nvim/plugged')

Plug 'chiel92/vim-autoformat'
Plug 'neoclide/coc.nvim', {'branch':'release'}
Plug 'preservim/nerdtree' |
            \ Plug 'Xuyuanp/nerdtree-git-plugin' |
            \ Plug 'ryanoasis/vim-devicons'
Plug 'chrisbra/colorizer'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'tpope/vim-surround'
Plug 'mattn/emmet-vim'
Plug 'preservim/nerdcommenter'
Plug 'majutsushi/tagbar'
Plug 'jiangmiao/auto-pairs'
Plug 'chrisbra/colorizer'
Plug 'tpope/vim-commentary'
Plug 'mboughaba/i3config.vim'
Plug 'honza/vim-snippets'
Plug 'glench/vim-jinja2-syntax'
Plug '907th/vim-auto-save'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'scrooloose/nerdtree'
Plug 'hiphish/jinja.vim'
Plug 'nvim-treesitter/nvim-treesitter'
Plug 'othree/html5.vim'

call plug#end()


imap <C-Q> <Esc>:q<CR>
imap <C-X> <Esc>:q!<CR>
imap <C-S> <Esc>:w<CR>a
nmap <C-Q> :q<CR>
nmap <C-X> :q!<CR>
nmap <C-S> :w<CR>
nmap <F12> :tabnew

" Setting bracket highlighting colors:
hi MatchParen cterm=none ctermbg=green ctermfg=blue
" Setting spell check colors
hi SpellBad cterm=none ctermbg=1 ctermfg=white
hi SpellCap cterm=none ctermbg=6 ctermfg=white
hi SpellRare cterm=none ctermbg=6 ctermfg=white
hi SpellLocal cterm=none ctermbg=6 ctermfg=white
