<template>
  <div class="file-tree">
    <TreeNode 
      v-for="(node, index) in tree" 
      :key="index" 
      :node="node" 
      :depth="0"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';

// ファイルツリーの構造を定義
const tree = ref([
  {
    name: '.claude',
    type: 'folder',
    expanded: true,
  },
  {
    name: '.devcontainer',
    type: 'folder',
    expanded: true,
    children: [
      { name: 'devcontainer.json', type: 'file' }
    ]
  },
  {
    name: '.vscode',
    type: 'folder',
    expanded: true,
  },
  {
    name: 'node_modules',
    type: 'folder',
    expanded: false,
  },
  {
    name: 'packages',
    type: 'folder',
    expanded: true,
    children: [
      {
        name: 'slides',
        type: 'folder',
        expanded: true,
        children: [
          { name: 'whats-cloudassembly', type: 'file' }
        ]
      },
      {
        name: 'components',
        type: 'folder',
        expanded: true,
        children: [
          { name: 'Columns.vue', type: 'file', modified: true },
          { name: 'Counter.vue', type: 'file', modified: true },
          { name: 'Highlight.vue', type: 'file', modified: true },
          { name: 'Note.vue', type: 'file', modified: true },
          { name: 'Overlay.vue', type: 'file', modified: true },
        ]
      }
    ]
  },
]);
</script>

<script>
export default {
  name: 'FileTree',
  components: {
    TreeNode: {
      name: 'TreeNode',
      props: {
        node: {
          type: Object,
          required: true
        },
        depth: {
          type: Number,
          default: 0
        }
      },
      data() {
        return {
          isExpanded: this.node.expanded ?? true
        };
      },
      methods: {
        toggle() {
          if (this.node.type === 'folder') {
            this.isExpanded = !this.isExpanded;
          }
        }
      },
      template: `
        <div class="tree-node">
          <div 
            class="tree-node-content" 
            :style="{ paddingLeft: (depth * 16) + 'px' }"
            @click="toggle"
          >
            <span v-if="node.type === 'folder'" class="tree-icon">
              {{ isExpanded ? '▼' : '▶' }}
            </span>
            <span v-else class="tree-icon-spacer"></span>
            
            <span class="tree-emoji">
              {{ node.type === 'folder' ? '📁' : '📄' }}
            </span>
            
            <span class="tree-label" :class="{ 'modified': node.modified }">
              {{ node.name }}
            </span>
            
            <span v-if="node.modified" class="modified-indicator">U</span>
          </div>
          
          <div v-if="node.children && isExpanded" class="tree-children">
            <TreeNode 
              v-for="(child, index) in node.children" 
              :key="index" 
              :node="child" 
              :depth="depth + 1"
            />
          </div>
        </div>
      `
    }
  }
};
</script>

<style scoped>
.file-tree {
  background-color: #1e1e1e;
  color: #cccccc;
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  padding: 8px 0;
  border-radius: 4px;
  user-select: none;
  max-width: 400px;
}

.tree-node-content {
  display: flex;
  align-items: center;
  padding: 2px 8px;
  cursor: pointer;
  transition: background-color 0.15s;
}

.tree-node-content:hover {
  background-color: #2a2d2e;
}

.tree-icon {
  width: 16px;
  font-size: 10px;
  color: #cccccc;
  margin-right: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.tree-icon-spacer {
  width: 16px;
  margin-right: 4px;
  display: inline-block;
}

.tree-emoji {
  margin-right: 6px;
  font-size: 14px;
}

.tree-label {
  flex: 1;
  color: #cccccc;
  white-space: nowrap;
}

.tree-label.modified {
  color: #73c991;
}

.modified-indicator {
  margin-left: auto;
  color: #73c991;
  font-size: 11px;
  font-weight: bold;
  padding-left: 8px;
}

.tree-children {
  /* Children are rendered with increased depth padding */
}
</style>