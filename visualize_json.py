import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.collections import LineCollection
from shapely.geometry import Polygon

def visualize_schema():
    try:
        with open("NAME.json", 'r') as f: # ПОЛОЖИТЕ СВОЙ ФАЙЛ В ДИРЕКТОРИЮ СО СКРИПТОМ И УКАЖИТЕ НАЗВАНИЕ
            data = json.load(f)
    except FileNotFoundError:
        print("ERROR: File not found")
        return
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return

    if not data.get('nodes'):
        print("ERROR: No nodes data")
        return

    all_x = [node['x'] for node in data['nodes']]
    all_y = [node['y'] for node in data['nodes']]
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    x_range = max_x - min_x
    y_range = max_y - min_y
    padding_x = max(x_range * 0.1, 5)
    padding_y = max(y_range * 0.1, 5)
    
    pos = {node['id']: (node['x'], node['y']) for node in data['nodes']}
    
    elements = {}
    for node in data['nodes']:
        if node['element_id'] not in elements:
            elements[node['element_id']] = []
        elements[node['element_id']].append(node)

    contour_edges = [(e['source'], e['target']) for e in data['edges'] if e['type'] == 'contour']

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_aspect('equal')
    
    ax.set_xlim(min_x - padding_x, max_x + padding_x)
    ax.set_ylim(min_y - padding_y, max_y + padding_y)
    
    if x_range > 0 and y_range > 0:
        range_max = max(x_range, y_range)
        
        if range_max <= 20:
            grid_step = 1
        elif range_max <= 50:
            grid_step = 5
        elif range_max <= 200:
            grid_step = 10
        else:
            grid_step = 20
        
        ax.xaxis.set_major_locator(mticker.MultipleLocator(grid_step))
        ax.yaxis.set_major_locator(mticker.MultipleLocator(grid_step))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='#b0b0b0', zorder=0)

        if grid_step >= 2:
            ax.xaxis.set_minor_locator(mticker.MultipleLocator(grid_step/2))
            ax.yaxis.set_minor_locator(mticker.MultipleLocator(grid_step/2))
            ax.grid(which='minor', linestyle=':', linewidth=0.4, color='#d0d0d0', zorder=0)
    else:
        ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(mticker.MultipleLocator(1))
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='#b0b0b0', zorder=0)
    
    if contour_edges:
        lines = [(pos[u], pos[v]) for u, v in contour_edges if u in pos and v in pos]
        if lines:
            ax.add_collection(LineCollection(lines, colors='#aaaaaa', linewidths=1.0, zorder=1))

    for el_id, nodes in elements.items():
        if len(nodes) > 2:
            nodes.sort(key=lambda n: n['id'])
            coords = [(n['x'], n['y']) for n in nodes]
            
            from matplotlib.patches import Polygon as MplPolygon
            poly = MplPolygon(coords, 
                            facecolor='#cceeff', 
                            edgecolor='#333333', 
                            linewidth=1.5, 
                            zorder=2, 
                            alpha=0.7)
            ax.add_patch(poly)
            
            poly_shapely = Polygon(coords)
            center = poly_shapely.representative_point()
            ax.text(center.x, center.y, str(el_id), 
                   ha='center', va='center', 
                   fontsize=10, fontweight='bold', 
                   color='#004466', 
                   zorder=5)

    node_x = [node['x'] for node in data['nodes']]
    node_y = [node['y'] for node in data['nodes']]
    ax.scatter(node_x, node_y, s=50, c='#005b96', 
               edgecolor='black', linewidth=0.5, zorder=4)

    ax.set_xlabel('X координата', fontsize=12)
    ax.set_ylabel('Y координата', fontsize=12)
    ax.set_title('Визуализация топологии схемы', fontsize=16, color='black')

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    
    legend_elements = [
        Patch(facecolor='#cceeff', edgecolor='#333333', label='Элемент', alpha=0.7),
        Line2D([0], [0], color='#aaaaaa', lw=1, label='Контурное ребро'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#005b96', 
               markeredgecolor='black', markersize=8, label='Вершина')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', 
              bbox_to_anchor=(1.02, 1), borderaxespad=0., 
              facecolor='white', edgecolor='gray', fontsize='small',
              title='Обозначения')
    
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()

if __name__ == "__main__":
    visualize_schema()