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

colorscheme Monokai

" Use True Colors
if exists('+termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

let g:mapleader = "\<Space>"
let g:maplocalleader = ','

nnoremap <F5> :setlocal spell! spelllang=en_us<CR>
nnoremap <F6> 1z=
nnoremap <F7> ]s
inoremap <F5> <Esc>:setlocal spell! spelllang=en_us<CR>
inoremap <F6> <Esc>1z=

nnoremap <leader>ev :e ~/.config/nvim/custom_commands.vim<CR>
nnoremap <leader>sv :source ~/.config/nvim/custom_commands.vim<bar> :doautocmd BufRead<CR>

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

nnoremap gn :bn<cr>
nnoremap gp :bp<cr>
nnoremap gd :bd<cr>  

:command SpellcheckOn :set spell spelllang=en_us
:command SpellcheckOff :set nospell

:command Tab2 :set shiftwidth=2
:command Tab4 :set shiftwidth=4

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
