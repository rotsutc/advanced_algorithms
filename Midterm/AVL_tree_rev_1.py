import streamlit as st
import graphviz
import json
import random

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
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # 4 CASE CÂN BẰNG
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
            # Node found
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

    # ---------- SEARCH ----------
    def search(self, root, key):
        if not root:
            return None
        if key == root.mssv:
            return root
        if key < root.mssv:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)


# ------------------ VISUALIZE TREE ------------------

def visualize_tree(root):
    if not root:
        return graphviz.Digraph()

    dot = graphviz.Digraph()
    def add_nodes_edges(node):
        if not node:
            return

        node_label = f"MSSV:{node.mssv}\nH:{node.height}\nBF:{AVLTree().get_balance(node)}"
        dot.node(str(node.mssv), node_label)

        if node.left:
            dot.edge(str(node.mssv), str(node.left.mssv))
            add_nodes_edges(node.left)

        if node.right:
            dot.edge(str(node.mssv), str(node.right.mssv))
            add_nodes_edges(node.right)

    add_nodes_edges(root)
    return dot


# ------------------ RANDOM NAME GENERATION ------------------

ho_list = ["Nguyễn", "Trần", "Lê", "Phạm", "Huỳnh", "Hoàng", "Võ", "Đặng", "Bùi", "Đỗ"]
ten_list = ["Minh", "An", "Hải", "Hưng", "Khánh", "Long", "Nam", "Phúc", "Quân", "Tuấn",
            "Trang", "Vy", "Linh", "Nhi", "Hương", "Thảo", "Ngọc", "My", "Yến", "Hà"]

def random_name():
    return random.choice(ho_list) + " " + random.choice(ten_list)


# ------------------ STREAMLIT UI ------------------

st.title("📚 QUẢN LÝ SINH VIÊN – CÂY AVL")

if "tree" not in st.session_state:
    st.session_state.tree = AVLTree()
    st.session_state.root = None
    st.session_state.next_id = 1


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Thêm sinh viên", "❌ Xóa sinh viên", "🔍 Tìm kiếm",
    "🌳 Xem cây", "💾 Lưu & Đọc cây"
])

# ------------ TAB 1: THÊM SINH VIÊN ------------
with tab1:
    st.subheader("➕ Thêm sinh viên mới")
    name = st.text_input("Họ và tên:")

    gpa = st.number_input("Điểm trung bình (0–10):", min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Thêm sinh viên"):
        if name.strip() == "":
            st.error("Vui lòng nhập tên!")
        else:
            mssv = st.session_state.next_id
            gpa = round(gpa, 1)
            st.session_state.root = st.session_state.tree.insert(
                st.session_state.root, mssv, name, gpa
            )
            st.session_state.next_id += 1
            st.success(f"Đã thêm sinh viên MSSV = {mssv}")

    # Nút thêm ngẫu nhiên
    if st.button("📌 Thêm ngẫu nhiên"):
        mssv = st.session_state.next_id
        name = random_name()
        gpa = round(random.uniform(0, 10), 1)

        st.session_state.root = st.session_state.tree.insert(
            st.session_state.root, mssv, name, gpa
        )
        st.session_state.next_id += 1
        st.success(f"Đã thêm ngẫu nhiên MSSV = {mssv}, Tên: {name}, GPA: {gpa}")


# ------------ TAB 2: XÓA SINH VIÊN ------------
with tab2:
    st.subheader("❌ Xóa sinh viên")
    delete_id = st.number_input("Nhập MSSV cần xóa:", min_value=1, step=1)

    if st.button("Xóa"):
        # Kiểm tra tồn tại trước khi xóa
        found = st.session_state.tree.search(st.session_state.root, delete_id)

        if found:
            st.session_state.root = st.session_state.tree.delete(st.session_state.root, delete_id)
            st.success(f"Đã xóa MSSV = {delete_id}")
        else:
            st.error(f"MSSV = {delete_id} không tồn tại")


# ------------ TAB 3: TÌM KIẾM ------------
with tab3:
    st.subheader("🔍 Tìm kiếm sinh viên")
    search_id = st.number_input("Nhập MSSV:", min_value=1, step=1)

    if st.button("Tìm"):
        result = st.session_state.tree.search(st.session_state.root, search_id)
        if result:
            st.success(f"✔ Tìm thấy sinh viên:\n\n**Tên:** {result.name}\n**GPA:** {result.gpa}")
        else:
            st.error("Không tìm thấy sinh viên!")


# ------------ TAB 4: HIỂN THỊ CÂY ------------
with tab4:
    st.subheader("🌳 Cây AVL hiện tại ")
    dot = visualize_tree(st.session_state.root)
    st.graphviz_chart(dot)


# ------------ TAB 5: LƯU & ĐỌC CÂY ------------
with tab5:
    st.subheader("💾 Lưu và Đọc cây AVL")

    def save_tree_to_file(node):
        """Convert tree to list for JSON."""
        if not node:
            return None
        return {
            "mssv": node.mssv,
            "name": node.name,
            "gpa": node.gpa,
            "left": save_tree_to_file(node.left),
            "right": save_tree_to_file(node.right)
        }

    def load_tree_from_data(data):
        """Convert JSON data back to AVL tree."""
        if data is None:
            return None
        node = StudentNode(data["mssv"], data["name"], data["gpa"])
        node.left = load_tree_from_data(data["left"])
        node.right = load_tree_from_data(data["right"])
        return node

    # Nút lưu
    if st.button("💾 Lưu cây"):
        if st.session_state.root:
            tree_data = save_tree_to_file(st.session_state.root)
            with open("tree_data.json", "w", encoding="utf-8") as f:
                json.dump(tree_data, f, ensure_ascii=False, indent=4)
            st.success("Đã lưu cây vào file tree_data.json")
        else:
            st.error("Cây rỗng, không thể lưu.")

    # Nút đọc
    if st.button("📂 Đọc cây"):
        try:
            with open("tree_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            temp_root = load_tree_from_data(data)

            # rebuild AVL tree (re-insert to auto balance)
            st.session_state.root = None
            st.session_state.tree = AVLTree()
            st.session_state.next_id = 1

            def rebuild(node):
                if not node:
                    return
                st.session_state.root = st.session_state.tree.insert(
                    st.session_state.root, node.mssv, node.name, node.gpa)
                st.session_state.next_id = max(st.session_state.next_id, node.mssv + 1)
                rebuild(node.left)
                rebuild(node.right)

            rebuild(temp_root)

            st.success("Đã đọc và khôi phục cây AVL đúng cấu trúc!")
        except:
            st.error("Không tìm thấy file hoặc file lỗi.")
