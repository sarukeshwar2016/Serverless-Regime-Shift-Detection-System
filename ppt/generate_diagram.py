import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8.5, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 11)
ax.axis('off')

def draw_box(x, y, w, h, text, color):
    box = mpatches.FancyBboxPatch((x, y), w, h,
                                  boxstyle="round,pad=0.15,rounding_size=0.3",
                                  ec="#666666", fc=color, lw=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=11, family='sans-serif')

# Positions based on user's image
# Top left: Frontend
fx, fy = 1.0, 8.5
fw, fh = 3.5, 1.2
draw_box(fx, fy, fw, fh, "Frontend\nNext.js • React • Tailwind", "#d1f5d3")

# Middle left: Backend
bx, by = 1.5, 6.0
bw, bh = 2.5, 1.2
draw_box(bx, by, bw, bh, "Backend\nFastAPI • Python ML", "#fff4cc")

# Bottom left: Data
dx, dy = 1.0, 3.5
dw, dh = 3.5, 1.2
draw_box(dx, dy, dw, dh, "Data Store\nRedis & MongoDB", "#ffd6d6")

# Middle right: Jenkins
jx, jy = 6.0, 6.0
jw, jh = 3.5, 1.2
draw_box(jx, jy, jw, jh, "Jenkins CI/CD\n(Build • Test • Deploy)", "#ebd9ff")

# Bottom right: Docker
cx, cy = 5.0, 3.5
cw, ch = 4.0, 1.2
draw_box(cx, cy, cw, ch, "Docker + Docker Compose\n(Containerization)", "#d6e8ff")

# Bottom Bottom right: Deployed System
px, py = 5.5, 1.0
pw, ph = 3.0, 1.2
draw_box(px, py, pw, ph, "Deployed System\n(AWS EC2 Instance)", "#d4f5e8")

# Arrows
def draw_arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), 
                arrowprops=dict(arrowstyle='-|>', lw=1.5, color='#444444'))

def draw_line(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='#444444', lw=1.5)

# Frontend down to Backend
draw_arrow(2.0, 8.5, 2.0, 7.2)
# Backend up to Frontend
draw_arrow(3.0, 7.2, 3.0, 8.5)

# Backend down to Data
draw_arrow(2.0, 6.0, 2.0, 4.7)
# Data up to Backend
draw_arrow(3.0, 4.7, 3.0, 6.0)

# Jenkins down to Docker
draw_arrow(7.75, 6.0, 7.75, 4.7)

# Frontend right and down to Docker
draw_line(4.5, 9.1, 6.5, 9.1)
draw_arrow(6.5, 9.1, 6.5, 4.7)

# Backend right and down to Docker
draw_line(4.0, 6.6, 5.5, 6.6)
draw_arrow(5.5, 6.6, 5.5, 4.7)

# Docker down to Deployed System
draw_arrow(7.0, 3.5, 7.0, 2.2)

# Add "Figure 1: Architecture Diagram" at the bottom
ax.text(5.0, 0.3, "Figure 1: Architecture Diagram", ha='center', va='center', fontsize=10, style='italic', color='#004488')

plt.savefig(r'C:\D_Drive\regime-platform\ppt\Regime_Architecture_Diagram.png', dpi=300, bbox_inches='tight')
print("Diagram saved.")
