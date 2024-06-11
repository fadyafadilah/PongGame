from tkinter import *
#menginpor pustaka acak
import random

#menambahkan variabel global

#varibael global
# pengaturan jendela
WIDTH = 900
HEIGHT = 300
#pengaturan raket
#lebar raket
PAD_W = 10
#tinggi raket
PAD_H = 100
#pengaturan bola
#seberapa besar kecepatan bola yang akan meningkatkat di setiap pukulan
BALL_SPEED_UP = 1.05

#kecepatan bola maksimum
BALL_MAX_SPEED = 40
#radius bola
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

# skor permainan
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
# menambahkan varibael global untuk jarak antara tepi kanan lepangan permainan
right_line_distance = WIDTH - PAD_W

def update_score(player):
  global PLAYER_1_SCORE, PLAYER_2_SCORE
  if player == "right":
    PLAYER_1_SCORE += 1
    c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
  else:
    PLAYER_2_SCORE += 1
    c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
  global BALL_X_SPEED
  # meletakan bola pada bagian tengah
  c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
           HEIGHT/2-BALL_RADIUS/2,
           WIDTH/2+BALL_RADIUS/2,
           HEIGHT/2+BALL_RADIUS/2)
  BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)

# fungsi bola pantul
def bounce(action):
  global BALL_X_SPEED, BALL_Y_SPEED

  # memukul menggunakan raket
  if action == "strike":
    BALL_Y_SPEED = random.randrange(-10, 10)
    if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
      BALL_X_SPEED *= -BALL_SPEED_UP
    else:
      BALL_X_SPEED = -BALL_X_SPEED
  else:
    BALL_Y_SPEED = -BALL_Y_SPEED

# memasang jendela 
root = Tk()
root.title("Pong")

# area animasi
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()

# area lapangan bermain

# garis kiri
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
# garis kanan
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
# garis tengah
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

# pemasangan fasilitas permainan

#membuat bola
BALL = c.create_oval (WIDTH/2-BALL_RADIUS/2,
                      HEIGHT/2-BALL_RADIUS/2,
                      WIDTH/2+BALL_RADIUS/2,
                      HEIGHT/2+BALL_RADIUS/2, fill="white")
#raket kiri
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")

#raket yang teapat
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2,
                          PAD_H, width=PAD_W, fill="yellow")

p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20",
                         fill="white")

p_2_text = c.create_text(WIDTH/6, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font="Arial 20",
                         fill="white")

#menambahkan variabel global untuk kecepatan bola
#di seluruh
BALL_X_CHANGE = 20
# Secara vertikal
BALL_Y_CHANGE = 0

def move_ball():
  #membuat koordinat pada sisi sisi bola dan pusatnya
  ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
  ball_center = (ball_top + ball_bot) / 2

  #pentulan vertikal
  #jika kita berada pada jarak garis vertikal - cukup gerakkan bolanya
  if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
    c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
  #jika bola menyentuh sisi kanan atau kiri batas lapangan
  elif ball_right == right_line_distance or ball_left == PAD_W:
    # Memeriksa sisi kanan atau kiri yang kita sentuh
    if ball_right > WIDTH / 2:
      if c.coords(RIGHT_PAD) [1] < ball_center < c.coords(RIGHT_PAD)[3]:
        bounce("strike")
      else:
        update_score("left")
        spawn_ball()
    else:
      if c.coords(LEFT_PAD) [1] < ball_center < c.coords(LEFT_PAD) [3]:
        bounce("strike")
      else:
        update_score("right")
        spawn_ball()
  else:
    if ball_right > WIDTH / 2:
      c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
    else:
      c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
  if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
    bounce("ricochet")

#mengatur variabel global untuk kecepatan raket
#kecepatan gerak raket yang akan dilalui
PAD_SPEED = 20
#Kecepatan platfrom kiri
LEFT_PAD_SPEED = 0
#kecepatan raket yang tepat
RIGHT_PAD_SPEED = 0

#Fungsi pergerakan pada kedua raket
def move_pads():
  #untuk kenyamanan, mari kita ciptakan kosakata di mana raket sesuai dengan kecepatannya
  PADS = {LEFT_PAD: LEFT_PAD_SPEED,
          RIGHT_PAD: RIGHT_PAD_SPEED}
  for pad in PADS:
    #menggerakan aket dengan keceoatan tertentu
    c.move(pad, 0, PADS[pad])
    # jika raket bergerak keluar dari bidang permainan, letakkan kembali pada tempatnya
    if c.coords(pad)[1] < 0:
      c.move(pad, 0, -c.coords(pad)[1])
    elif c.coords(pad)[3] > HEIGHT:
      c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
  move_ball()
  move_pads()
  #memanggil dirinya sendiri pada setiap 30 milidetik
  root.after(30, main)

# mengatur fokus canvas untuk merespon penekanan tombol
c.focus_set()

#menulis fungsi untuk menangani penekanan pada tombol
def movement_handler(event):
  global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
  if event.keysym == "w":
    LEFT_PAD_SPEED == -PAD_SPEED
  elif event.keysym == "s":
    LEFT_PAD_SPEED == PAD_SPEED
  elif event.keysym == "Up":
    RIGHT_PAD_SPEED == -PAD_SPEED
  elif event.keysym == "Down":
    RIGHT_PAD_SPEED == PAD_SPEED

# mengikat fungsi ini ke canvas
c.bind("<KeyPress>", movement_handler)

# membuat fungsi respons pelepasan tombol
def stop_pad(event):
  global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
  if event.keysym in "ws":
    LEFT_PAD_SPEED = 0
  elif event.keysym in ("Up", "Down"):
    RIGHT_PAD_SPEED = 0

#mengikat fungsi ke canvas
c.bind("<KeyRelease>", stop_pad)

#pengaturan dalam gerakan
main()

#menjalankan jendela
root.mainloop()