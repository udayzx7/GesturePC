import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.mouse import Controller, Button
from PIL import ImageGrab
import math
import time

# =========================
# INIT
# =========================
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)  # Changed to 2 hands
mouse = Controller()

screenW, screenH = 1920, 1080

prevX, prevY = 0, 0
smooth = 5

drag = False
scrollStart = None
lastScroll = 0  # For dual-hand scroll
lastClick = 0
lastShot = 0

mode = "MOVE"   # MOVE / DRAG / SCROLL / SCREENSHOT_LOCK / DUAL_SCROLL

# =========================
# UI COLORS
# =========================
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
CYAN = (255, 255, 0)
YELLOW = (0, 255, 255)
PURPLE = (255, 0, 255)

# =========================
# HELPER FUNCTIONS
# =========================
def is_palm(hand):
    """Check if hand is open palm"""
    return detector.fingersUp(hand) == [1,1,1,1,1]

def is_scroll_pose(hand):
    """Check if hand has index and middle fingers up only"""
    fingers = detector.fingersUp(hand)
    return fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0

def is_fist(hand):
    """Check if hand is a fist"""
    fingers = detector.fingersUp(hand)
    return fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0

# =========================
# LOOP
# =========================
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Split hands
    leftHand = None
    rightHand = None
    
    if hands:
        for h in hands:
            if h["type"] == "Left":
                leftHand = h
            else:
                rightHand = h

    # =========================
    # DUAL-HAND SCROLL MODE (PRIORITY)
    # =========================
    if leftHand and rightHand:
        
        # SCROLL UP: Left palm + any right hand
        if is_palm(leftHand):
            mode = "DUAL_SCROLL_UP"
            if time.time() - lastScroll > 0.2:
                mouse.scroll(0, 3)   # UP
                lastScroll = time.time()
                cv2.putText(img, "SCROLL UP (Left Palm)", (40, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, GREEN, 2)

        # SCROLL DOWN: Right palm + Left index-middle up
        elif is_palm(rightHand) and leftHand and is_scroll_pose(leftHand):
            mode = "DUAL_SCROLL_DOWN"
            if time.time() - lastScroll > 0.2:
                mouse.scroll(0, -3)  # DOWN
                lastScroll = time.time()
                cv2.putText(img, "SCROLL DOWN (Right Palm)", (40, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)
        else:
            # If no dual-hand scroll, proceed to single-hand control
            pass
    
    # =========================
    # SINGLE-HAND CONTROL (if no dual-hand scroll active)
    # =========================
    if hands and not (leftHand and rightHand and (is_palm(leftHand) or (is_palm(rightHand) and leftHand and is_scroll_pose(leftHand)))):
        
        # Use the first available hand for single-hand control
        hand = hands[0]
        lm = hand["lmList"]
        fingers = detector.fingersUp(hand)

        thumb = lm[4]
        index = lm[8]
        middle = lm[12]
        ring = lm[16]
        pinky = lm[20]

        tx, ty = thumb[0], thumb[1]
        ix, iy = index[0], index[1]
        mx, my = middle[0], middle[1]
        rx, ry = ring[0], ring[1]
        px, py = pinky[0], pinky[1]

        # =========================
        # DISTANCES
        # =========================
        t_i = math.hypot(tx - ix, ty - iy)
        t_m = math.hypot(tx - mx, ty - my)
        t_p = math.hypot(tx - px, ty - py)

        # =========================
        # PRIORITY SYSTEM
        # =========================

        # ---------- 1. DRAG MODE ----------
        if t_p < 40 and t_i > 40:
            mode = "DRAG"
            if not drag:
                mouse.press(Button.left)
                drag = True

        else:
            if drag:
                mouse.release(Button.left)
                drag = False

        # ---------- 2. SCROLL MODE ----------
        if is_scroll_pose(hand):
            mode = "SCROLL"

            if scrollStart is None:
                scrollStart = time.time()

            hold = time.time() - scrollStart

            if hold > 2:
                if iy < 250:
                    mouse.scroll(0, 3)
                    cv2.putText(img, "SCROLL UP", (40, 300),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, CYAN, 2)

                elif iy > 450:
                    mouse.scroll(0, -3)
                    cv2.putText(img, "SCROLL DOWN", (40, 300),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)

        else:
            scrollStart = None

        # ---------- 3. SCREENSHOT (FIST) ----------
        if is_fist(hand):
            mode = "SCREENSHOT"

            if time.time() - lastShot > 3:
                imgShot = ImageGrab.grab()
                name = f"shot_{int(time.time())}.png"
                imgShot.save(name)
                lastShot = time.time()
                cv2.putText(img, "SCREENSHOT TAKEN!", (40, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, YELLOW, 2)

        # ---------- Reset mode if no gesture ----------
        if t_p >= 40 and not is_scroll_pose(hand) and not is_fist(hand):
            mode = "MOVE"

        # ---------- 4. CLICK ----------
        if mode == "MOVE":
            # LEFT CLICK
            if t_i < 30 and time.time() - lastClick > 0.6:
                mouse.click(Button.left, 1)
                lastClick = time.time()
                cv2.putText(img, "LEFT CLICK", (40, 360),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2)

            # RIGHT CLICK
            if t_m < 30 and time.time() - lastClick > 0.6:
                mouse.click(Button.right, 1)
                lastClick = time.time()
                cv2.putText(img, "RIGHT CLICK", (40, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED, 2)

        # =========================
        # CURSOR MOVE (MOVE or DRAG mode)
        # =========================
        if mode == "MOVE" or mode == "DRAG":
            sx = int(screenW / 1280 * ix)
            sy = int(screenH / 720 * iy)

            cx = prevX + (sx - prevX) / smooth
            cy = prevY + (sy - prevY) / smooth

            mouse.position = (cx, cy)

            prevX, prevY = cx, cy

            cv2.circle(img, (ix, iy), 12, PURPLE, cv2.FILLED)

        # =========================
        # UI TEXT FOR SINGLE HAND
        # =========================
        
        # Mode display with color coding
        if mode == "DRAG":
            mode_color = RED
        elif mode == "SCROLL":
            mode_color = CYAN
        elif mode == "SCREENSHOT":
            mode_color = YELLOW
        else:
            mode_color = GREEN
            
        cv2.putText(img, f"MODE: {mode}", (40, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, mode_color, 2)

        if drag:
            cv2.putText(img, "DRAG ACTIVE", (40, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, RED, 2)

        if scrollStart is not None:
            hold_time = time.time() - scrollStart
            if hold_time < 2:
                cv2.putText(img, f"SCROLL READY: {2-hold_time:.1f}s", (40, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, CYAN, 2)
            else:
                cv2.putText(img, "SCROLL ACTIVE (move up/down)", (40, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, CYAN, 2)

        if is_fist(hand):
            cv2.putText(img, "FIST = SCREENSHOT", (40, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW, 2)

    # =========================
    # UI TEXT (Always visible)
    # =========================
    
    if leftHand and rightHand:
        cv2.putText(img, "DUAL HAND MODE ACTIVE", (40, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2)
        cv2.putText(img, "Left Palm = Scroll UP | Right Palm + Left Index-Middle = Scroll DOWN",
                    (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 2)
    
    # Show gesture hints
    cv2.putText(img, "Uday Garasiya:", (40, 500),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)
    cv2.putText(img, "Move: Index up | Drag: Thumb+Pinky | Scroll: Index+Middle (Hold)", 
                (40, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    cv2.putText(img, "Left Click: Thumb+Index | Right Click: Thumb+Middle | Screenshot: Fist", 
                (40, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    
    if leftHand and rightHand:
        cv2.putText(img, "DUAL-HAND SCROLL: Left Palm (UP) | Right Palm + Left 2 Fingers (DOWN)", 
                    (40, 590), cv2.FONT_HERSHEY_SIMPLEX, 0.5, CYAN, 1)

    # =========================
    # SHOW
    # =========================
    cv2.imshow("V", img)

    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()