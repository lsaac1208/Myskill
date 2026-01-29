#!/usr/bin/env node
/**
 * 本地搜索 MCP 服务器 - 通过调用 Python 脚本
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';

const server = new Server(
  {
    name: 'local-search',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 调用 Python 搜索脚本
function searchPython(query) {
  return new Promise((resolve, reject) => {
    const pythonScript = '/Users/wang/.claude/skills/local-search/scripts/local_search.py';
    const process = spawn('python3', [pythonScript, 'search', query, '--json']);

    let output = '';
    let error = '';

    process.stdout.on('data', (data) => {
      output += data.toString();
    });

    process.stderr.on('data', (data) => {
      error += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve(output);
      } else {
        reject(new Error(error || '搜索失败'));
      }
    });
  });
}

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'search',
        description: '使用 DuckDuckGo 进行本地网络搜索，不消耗 GLM MCP 额度',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: '搜索关键词',
            },
          },
          required: ['query'],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: { query } } = request.params;

  if (name === 'search') {
    try {
      const output = await searchPython(query);
      return {
        content: [{
          type: 'text',
          text: output,
        }],
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `搜索失败: ${error.message}`,
        }],
      };
    }
  }

  throw new Error(`未知工具: ${name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
