import os
import sys
import pygame as pg
import random, time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, +5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(+5, 0)}

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
	variable: koukaton_rect/bomb_rect
	return : tuple (vertical, horizontal)
	True if inside, False if outside
	"""
    hor, ver = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        hor = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        ver = False
    return hor, ver

def gameover(screen: pg.Surface) -> None:
    """
    display gameover screen when touch the bomb
    """

    gg_bg = pg.Surface([WIDTH, HEIGHT])
    gg_bg.set_alpha (150)
    screen.blit(gg_bg,[0,0])

    gg_font = pg.font.Font(None,80)
    txt = gg_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(txt, [400, 300])
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img, [350, 300])
    screen.blit(kk_img, [750, 300])
    pg.display.update()
    time.sleep(5)
    return


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    return: tuple (bb_imgs, bb_accs)
    bomb getting bigger and faster with time
    """
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface ((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append ((bb_img))
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    #define bomb speed and size
    bb_imgs , bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]

    # bomb spawn in random position
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = (random.randint(0, WIDTH)) 
    bb_rct.centery = (random.randint(0, HEIGHT))
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  #end game when touches the bomb
            gameover(screen)
            print ("game over")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, move in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += move[0]
                sum_mv[1] += move[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):  #return kk move if hits the walls
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # bomb grow bigger and faster with time 
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        hor, ver = check_bound(bb_rct)
        if not hor:
            vx *= -1
        if not ver:
            vy *= -1
        screen.blit(bb_img, bb_rct) 

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
