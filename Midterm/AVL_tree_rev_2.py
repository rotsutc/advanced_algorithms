import streamlit as st
import graphviz
import random
import pandas as pd

# ------------------ AVL TREE IMPLEMENTATION ------------------

class StudentNode:
    def __init__(self, mssv, name, gpa):
        self.mssv = mssv
        self.name = name
        self.gpa = gpa
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    # ---------- ROTATIONS ----------
    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # ---------- INSERT ----------
    def insert(self, root, mssv, name, gpa):
        if not root:
            return StudentNode(mssv, name, gpa)

        if mssv < root.mssv:
            root.left = self.insert(root.left, mssv, name, gpa)
        elif mssv > root.mssv:
            root.right = self.insert(root.right, mssv, name, gpa)
        else:
            # duplicate IDs not allowed
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # 4 CASES
        if balance > 1 and mssv < root.left.mssv:
            return self.right_rotate(root)
        if balance < -1 and mssv > root.right.mssv:
            return self.left_rotate(root)
        if balance > 1 and mssv > root.left.mssv:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and mssv < root.right.mssv:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # ---------- FIND MIN ----------
    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    # ---------- DELETE ----------
    def delete(self, root, key):
        if not root:
            return root

        if key < root.mssv:
            root.left = self.delete(root.left, key)
        elif key > root.mssv:
            root.right = self.delete(root.right, key)
        else:
            # Node to be deleted found
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.mssv = temp.mssv
            root.name = temp.name
            root.gpa = temp.gpa
            root.right = self.delete(root.right, temp.mssv)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Rebalance
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # ---------- SEARCH (returns node and path) ----------
    def search_with_path(self, root, key):
        path = []
        node = root
        while node:
            path.append(node.mssv)
            if key == node.mssv:
                return node, path
            elif key < node.mssv:
                node = node.left
            else:
                node = node.right
        return None, path

# ------------------ UTILITIES ------------------

ho_list = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng", "Bùi", "Đỗ"]
ten_list = ["Minh", "An", "Hải", "Hưng", "Khánh", "Long", "Nam", "Phúc", "Quân", "Tuấn",
            "Trang", "Vy", "Linh", "Nhi", "Hương", "Thảo", "Ngọc", "My", "Yến", "Hà"]

def random_name():
    return random.choice(ho_list) + " " + random.choice(ten_list)

def inorder_list(node, acc):
    if not node:
        return
    inorder_list(node.left, acc)
    acc.append({"mssv": node.mssv, "name": node.name, "gpa": node.gpa})
    inorder_list(node.right, acc)

def collect_nodes(node, nodes):
    if not node:
        return
    nodes.append(node)
    collect_nodes(node.left, nodes)
    collect_nodes(node.right, nodes)

def compute_depths(root):
    depths = {}
    def dfs(node, d):
        if not node:
            return
        depths[node.mssv] = d
        dfs(node.left, d+1)
        dfs(node.right, d+1)
    dfs(root, 0)
    return depths

# ------------------ VISUALIZATION ------------------

def bf_color(bf):
    # BF = 0: green; BF = ±1: yellow; |BF|>=2: red
    if bf == 0:
        return "lightgreen"
    if abs(bf) == 1:
        return "lightgoldenrodyellow"
    return "lightcoral"

def visualize_tree(root, highlight_path=None):
    dot = graphviz.Digraph(format="png")
    if not root:
        return dot

    depths = compute_depths(root)
    nodes = []
    collect_nodes(root, nodes)

    # Create nodes with record label: {depth | mssv | BF}
    for n in nodes:
        bf = AVLTree().get_balance(n)
        depth = depths.get(n.mssv, 0)
        label = "{{ {} | {} | BF:{} }}".format(depth, n.mssv, bf)
        style = "filled"
        fillcolor = bf_color(bf)
        dot.node(str(n.mssv), label=label, shape="record", style=style, fillcolor=fillcolor)

    # Create edges; highlight edges along path if provided
    def add_edges(node):
        if not node:
            return
        if node.left:
            attrs = {}
            if highlight_path and (node.mssv in highlight_path and node.left.mssv in highlight_path):
                try:
                    i = highlight_path.index(node.mssv)
                    if (i+1 < len(highlight_path) and highlight_path[i+1] == node.left.mssv) or (i>0 and highlight_path[i-1] == node.left.mssv):
                        attrs = {"color":"red", "penwidth":"2"}
                except (ValueError, IndexError):
                    attrs = {}
            dot.edge(str(node.mssv), str(node.left.mssv), **attrs)
            add_edges(node.left)
        if node.right:
            attrs = {}
            if highlight_path and (node.mssv in highlight_path and node.right.mssv in highlight_path):
                try:
                    i = highlight_path.index(node.mssv)
                    if (i+1 < len(highlight_path) and highlight_path[i+1] == node.right.mssv) or (i>0 and highlight_path[i-1] == node.right.mssv):
                        attrs = {"color":"red", "penwidth":"2"}
                except (ValueError, IndexError):
                    attrs = {}
            dot.edge(str(node.mssv), str(node.right.mssv), **attrs)
            add_edges(node.right)
    add_edges(root)
    return dot

# ------------------ SAVE / LOAD TREE ------------------

def tree_to_dict(node):
    if not node:
        return None
    return {
        "mssv": node.mssv,
        "name": node.name,
        "gpa": node.gpa,
        "left": tree_to_dict(node.left),
        "right": tree_to_dict(node.right)
    }

def dict_to_tree(data):
    if data is None:
        return None
    node = StudentNode(data["mssv"], data["name"], data["gpa"])
    node.left = dict_to_tree(data.get("left"))
    node.right = dict_to_tree(data.get("right"))
    # height will be recalculated when rebuilding via insert for balance
    return node

# ------------------ STREAMLIT UI ------------------

st.set_page_config(page_title="Quản lý sinh viên - AVL", layout="wide")

st.title("📚 QUẢN LÝ SINH VIÊN – CÂY AVL")

if "tree_obj" not in st.session_state:
    st.session_state.tree_obj = AVLTree()
    st.session_state.root = None
    st.session_state.next_id = 1

# Layout: tabs
# tabs = st.tabs(["➕ Thêm", "❌ Xóa", "✏️ Cập nhật", "🔍 Tìm kiếm", "🌳 Xem cây", "💾 Lưu/Đọc & Xuất"])
# tab_add, tab_delete, tab_update, tab_search, tab_view, tab_save = tabs
tabs = st.tabs(["➕ Thêm", "❌ Xóa", "✏️ Cập nhật", "🔍 Tìm kiếm", "🌳 Xem cây"])
tab_add, tab_delete, tab_update, tab_search, tab_view = tabs

# ---------------- TAB: ADD ----------------
with tab_add:
    st.header("➕ Thêm sinh viên")
    with st.form("add_form", clear_on_submit=False):
        name = st.text_input("Họ và tên")
        gpa = st.number_input("Điểm trung bình (0–10, 1 chữ số):", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
        submitted = st.form_submit_button("Thêm sinh viên")
        if submitted:
            if name.strip() == "":
                st.error("Vui lòng nhập tên.")
            else:
                mssv = st.session_state.next_id
                gpa = round(float(gpa), 1)
                st.session_state.root = st.session_state.tree_obj.insert(st.session_state.root, mssv, name, gpa)
                st.session_state.next_id += 1
                st.success(f"Đã thêm sinh viên MSSV = {mssv}")
    

    if st.button("📌 Thêm ngẫu nhiên"):
        mssv = st.session_state.next_id
        name = random_name()
        gpa = round(random.uniform(0, 10), 1)
        st.session_state.root = st.session_state.tree_obj.insert(st.session_state.root, mssv, name, gpa)
        st.session_state.next_id += 1
        st.success(f"Đã thêm ngẫu nhiên MSSV = {mssv} — {name} — GPA: {gpa}")

# ---------------- TAB: DELETE ----------------
with tab_delete:
    st.header("❌ Xóa sinh viên")
    col1, col2 = st.columns([2,1])
    with col1:
        del_id = st.number_input("Nhập MSSV cần xóa:", min_value=1, step=1, value=1)
    with col2:
        if st.button("Xóa"):
            node, _ = st.session_state.tree_obj.search_with_path(st.session_state.root, del_id)
            if node:
                st.session_state.root = st.session_state.tree_obj.delete(st.session_state.root, del_id)
                st.success(f"Đã xóa MSSV = {del_id}")
            else:
                st.error(f"MSSV = {del_id} không tồn tại")

        if st.button("🧹 Xóa toàn bộ"):
            st.session_state.root = None
            st.session_state.next_id = 1
            st.success("Đã xóa toàn bộ sinh viên (cây rỗng).")

# ---------------- TAB: UPDATE ----------------
with tab_update:
    st.header("✏️ Cập nhật sinh viên")
    up_id = st.number_input("Nhập MSSV cần cập nhật:", min_value=1, step=1, value=1, key="up_id")
    if st.button("Tìm để cập nhật"):
        node, path = st.session_state.tree_obj.search_with_path(st.session_state.root, up_id)
        if node:
            st.session_state._edit_node = {"mssv": node.mssv, "name": node.name, "gpa": node.gpa}
            st.success("Tìm thấy sinh viên — bạn có thể chỉnh sửa thông tin bên dưới.")
        else:
            st.error("Không tìm thấy MSSV để cập nhật.")

    if "_edit_node" in st.session_state:
        edit = st.session_state._edit_node
        new_name = st.text_input("Họ và tên:", value=edit["name"], key="edit_name")
        new_gpa = st.number_input("Điểm trung bình (0–10, 1 chữ số):", min_value=0.0, max_value=10.0, step=0.1,
                                  value=float(edit["gpa"]), key="edit_gpa", format="%.1f")
        if st.button("Cập nhật"):
            # find node, update fields
            node, _ = st.session_state.tree_obj.search_with_path(st.session_state.root, edit["mssv"])
            if node:
                node.name = new_name.strip() if new_name.strip()!="" else node.name
                node.gpa = round(float(new_gpa), 1)
                st.success(f"Đã cập nhật MSSV = {node.mssv}")
                # clear edit state
                del st.session_state["_edit_node"]
            else:
                st.error("Lỗi: không tìm thấy node khi cập nhật.")

# ---------------- TAB: SEARCH ----------------
with tab_search:
    st.header("🔍 Tìm kiếm sinh viên")
    s_id = st.number_input("Nhập MSSV:", min_value=1, step=1, value=1, key="search_id")
    if st.button("Tìm"):
        node, path = st.session_state.tree_obj.search_with_path(st.session_state.root, s_id)
        if node:
            st.success(f"✔ Tìm thấy: MSSV={node.mssv} — Tên: {node.name} — GPA: {node.gpa}")
            st.write("Đường đi (MSSV visited):", " → ".join(map(str, path)))
            # visualize with highlighted path
            dot = visualize_tree(st.session_state.root, highlight_path=path)
            st.graphviz_chart(dot)
        else:
            st.error("Không tìm thấy sinh viên!")
            # visualize tree without highlight
            dot = visualize_tree(st.session_state.root)
            st.graphviz_chart(dot)

# ---------------- TAB: VIEW TREE ----------------
with tab_view:
    st.header("🌳 Xem cây AVL hiện tại")
    # Show tree
    dot = visualize_tree(st.session_state.root)
    st.graphviz_chart(dot)

    st.markdown("### 📋 Danh sách sinh viên (bảng - theo MSSV)")
    students = []
    inorder_list(st.session_state.root, students)
    if students:
        df = pd.DataFrame(students).sort_values("mssv").reset_index(drop=True)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
                            label="📥 Tải CSV danh sách sinh viên",
                            data=csv,
                            file_name="danh_sach_sinh_vien.csv",
                            mime="text/csv",
                            key=f"download_csv_{len(df)}"   # khóa thay đổi mỗi lần render
                        )
    else:
        st.info("Không có sinh viên để hiển thị.")

    