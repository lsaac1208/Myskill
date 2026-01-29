---
name: awesome-workflow-engines
description: 工作流引擎查询时自动触发 - workflow engine、工作流引擎、任务编排、workflow、airflow、argo、dagster、任务调度。精选开源工作流引擎列表，提供各类工作流编排工具的查询和搜索功能。
github_url: https://github.com/meirwah/awesome-workflow-engines
github_hash: 202f3b9fe7b467b22fa38f52438fb8a7a6f2d03e
version: 0.2.0
created_at: 2026-01-25T14:21:13.485033
updated_at: 2026-01-26
entry_point: scripts/wrapper.py
dependencies: []
license: Unknown
---

# Awesome Workflow Engines Skill

精选开源工作流引擎大全，涵盖各类任务编排和工作流管理工具。

## 🎯 适用场景

当用户请求以下内容时自动激活此 Skill：

- **工作流引擎**: "workflow engine"、"工作流引擎"、"任务编排"
- **任务调度**: "任务调度"、"作业调度"、"定时任务"
- **数据管道**: "数据管道"、"ETL"、"数据处理"
- **自动化**: "流程自动化"、"业务流程"、"工作流自动化"

## ✨ 核心功能

- ✅ **分类全面**: 涵盖各类工作流引擎
- ✅ **技术多样**: 支持多种编程语言
- ✅ **场景丰富**: 适用于不同业务场景
- ✅ **开源免费**: 精选开源项目
- ✅ **社区活跃**: 有活跃的社区支持
- ✅ **生产就绪**: 可用于生产环境

## 🚀 工作流引擎分类

### 🔥 通用工作流引擎

#### Apache Airflow
**描述**: 最流行的数据工作流平台

**特点**:
- Python 编写，易于扩展
- 丰富的操作符和传感器
- 强大的调度和监控
- 活跃的社区和生态

**适用场景**:
- 数据管道编排
- ETL 任务调度
- 机器学习工作流
- 批处理任务

**示例**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

with DAG(
    'etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )

    extract_task >> transform_task >> load_task
```

#### Prefect
**描述**: 现代化的数据工作流平台

**特点**:
- Python 原生，代码即配置
- 动态工作流
- 云原生架构
- 优秀的错误处理

**适用场景**:
- 数据工程
- MLOps
- 自动化脚本
- 复杂数据管道

**示例**:
```python
from prefect import flow, task

@task
def extract():
    print("Extracting data...")
    return {"data": [1, 2, 3]}

@task
def transform(data):
    print("Transforming data...")
    return [x * 2 for x in data["data"]]

@task
def load(data):
    print(f"Loading data: {data}")

@flow
def etl_pipeline():
    raw_data = extract()
    transformed = transform(raw_data)
    load(transformed)

if __name__ == "__main__":
    etl_pipeline()
```

#### Temporal
**描述**: 可靠的微服务编排平台

**特点**:
- 强大的状态管理
- 自动重试和恢复
- 支持长时间运行的工作流
- 多语言支持

**适用场景**:
- 微服务编排
- 分布式事务
- 长时间运行的业务流程
- 可靠的任务执行

### ☁️ 云原生工作流

#### Argo Workflows
**描述**: Kubernetes 原生的工作流引擎

**特点**:
- 容器原生
- DAG 和步骤工作流
- 与 Kubernetes 深度集成
- 支持并行执行

**适用场景**:
- CI/CD 流水线
- 机器学习训练
- 批处理作业
- 数据处理

**示例**:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-
spec:
  entrypoint: whalesay
  templates:
  - name: whalesay
    container:
      image: docker/whalesay
      command: [cowsay]
      args: ["hello world"]
```

#### Flyte
**描述**: 可扩展的机器学习和数据处理平台

**特点**:
- 强类型工作流
- 版本控制
- 资源管理
- 多云支持

**适用场景**:
- 机器学习工作流
- 数据处理管道
- 批量计算
- 科学计算

#### Tekton
**描述**: Kubernetes 原生的 CI/CD 框架

**特点**:
- 云原生
- 可重用的组件
- 声明式配置
- 与 Kubernetes 集成

**适用场景**:
- CI/CD 流水线
- 容器构建
- 应用部署
- 自动化测试

### 📊 数据工作流

#### Dagster
**描述**: 数据编排平台

**特点**:
- 数据感知
- 类型系统
- 测试和验证
- 丰富的 UI

**适用场景**:
- 数据管道
- 数据质量
- 数据转换
- 分析工作流

**示例**:
```python
from dagster import asset, Definitions

@asset
def extract_data():
    return {"data": [1, 2, 3, 4, 5]}

@asset
def transform_data(extract_data):
    return [x * 2 for x in extract_data["data"]]

@asset
def load_data(transform_data):
    print(f"Loading: {transform_data}")

defs = Definitions(
    assets=[extract_data, transform_data, load_data]
)
```

#### Luigi
**描述**: Python 批处理框架

**特点**:
- 简单易用
- 依赖管理
- 可视化界面
- 轻量级

**适用场景**:
- 批处理任务
- 数据管道
- 报表生成
- 文件处理

#### Kedro
**描述**: 数据科学工作流框架

**特点**:
- 模块化设计
- 数据目录
- 管道可视化
- 最佳实践

**适用场景**:
- 数据科学项目
- 机器学习管道
- 数据工程
- 实验管理

### 🤖 业务流程管理

#### Camunda
**描述**: 企业级工作流和决策自动化平台

**特点**:
- BPMN 2.0 标准
- DMN 决策引擎
- 可视化建模
- 企业级功能

**适用场景**:
- 业务流程自动化
- 审批流程
- 订单处理
- 企业应用集成

#### Activiti
**描述**: 轻量级的业务流程引擎

**特点**:
- BPMN 2.0 支持
- Spring 集成
- 易于嵌入
- 活跃社区

**适用场景**:
- 工作流管理
- 业务流程
- 审批系统
- 任务管理

#### Flowable
**描述**: 现代化的业务流程引擎

**特点**:
- BPMN、CMMN、DMN 支持
- 高性能
- 云就绪
- 丰富的 API

**适用场景**:
- 复杂业务流程
- 案例管理
- 决策自动化
- 流程优化

### 🔄 事件驱动工作流

#### Conductor (Netflix)
**描述**: 微服务编排引擎

**特点**:
- 可视化工作流
- 动态工作流
- 任务重试
- 监控和追踪

**适用场景**:
- 微服务编排
- 异步任务
- 分布式系统
- 事件处理

#### Cadence (Uber)
**描述**: 分布式、可扩展的编排引擎

**特点**:
- 容错性强
- 可扩展
- 状态管理
- 长时间运行

**适用场景**:
- 微服务编排
- 分布式事务
- 业务流程
- 状态机

### 🎯 轻量级工作流

#### n8n
**描述**: 工作流自动化工具

**特点**:
- 可视化编辑器
- 丰富的集成
- 自托管
- 易于使用

**适用场景**:
- 自动化任务
- API 集成
- 数据同步
- 通知和提醒

#### Windmill
**描述**: 开源的开发者平台

**特点**:
- 代码即工作流
- 多语言支持
- 自动生成 UI
- 快速部署

**适用场景**:
- 内部工具
- 自动化脚本
- API 编排
- 数据处理

## 📋 工作流引擎对比

### 按语言分类

| 语言 | 工作流引擎 |
|------|-----------|
| **Python** | Airflow, Prefect, Dagster, Luigi, Kedro |
| **Go** | Temporal, Cadence, Argo Workflows |
| **Java** | Camunda, Activiti, Flowable, Conductor |
| **JavaScript** | n8n, Node-RED |
| **多语言** | Temporal, Flyte, Argo Workflows |

### 按场景分类

| 场景 | 推荐引擎 |
|------|---------|
| **数据管道** | Airflow, Prefect, Dagster |
| **机器学习** | Flyte, Kubeflow, Metaflow |
| **CI/CD** | Argo Workflows, Tekton, Jenkins X |
| **微服务编排** | Temporal, Conductor, Cadence |
| **业务流程** | Camunda, Activiti, Flowable |
| **自动化任务** | n8n, Windmill, Zapier |

### 按规模分类

| 规模 | 推荐引擎 |
|------|---------|
| **小型项目** | Luigi, n8n, Windmill |
| **中型项目** | Prefect, Dagster, Argo Workflows |
| **大型项目** | Airflow, Temporal, Camunda |
| **企业级** | Camunda, Flowable, Temporal |

## 🔧 选择指南

### 数据工程场景

**推荐**: Airflow, Prefect, Dagster

**理由**:
- 专为数据管道设计
- 丰富的数据源集成
- 强大的调度功能
- 完善的监控和告警

**选择建议**:
```markdown
- **Airflow**: 成熟稳定，生态丰富，适合大规模数据管道
- **Prefect**: 现代化设计，易于使用，适合快速开发
- **Dagster**: 数据感知，类型安全，适合数据质量要求高的场景
```

### 机器学习场景

**推荐**: Flyte, Kubeflow, Metaflow

**理由**:
- 支持 GPU 资源管理
- 实验追踪
- 模型版本控制
- 分布式训练

**选择建议**:
```markdown
- **Flyte**: 强类型，版本控制，适合大规模 ML 工作流
- **Kubeflow**: Kubernetes 原生，完整的 ML 平台
- **Metaflow**: 简单易用，适合数据科学家
```

### 微服务编排场景

**推荐**: Temporal, Conductor, Cadence

**理由**:
- 可靠的状态管理
- 自动重试和恢复
- 支持长时间运行
- 分布式事务

**选择建议**:
```markdown
- **Temporal**: 功能最全，社区活跃，适合复杂场景
- **Conductor**: 可视化好，易于监控，适合微服务编排
- **Cadence**: Uber 出品，稳定可靠，适合大规模部署
```

### 业务流程场景

**推荐**: Camunda, Activiti, Flowable

**理由**:
- BPMN 标准支持
- 可视化建模
- 企业级功能
- 审批流程

**选择建议**:
```markdown
- **Camunda**: 功能最全，企业级，适合复杂业务流程
- **Activiti**: 轻量级，易于集成，适合中小型项目
- **Flowable**: 现代化，性能好，适合云原生应用
```

## 📝 实用示例

### 示例 1: Airflow ETL 管道

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def extract_from_api():
    # 从 API 提取数据
    import requests
    response = requests.get('https://api.example.com/data')
    return response.json()

def transform_data(**context):
    # 转换数据
    data = context['task_instance'].xcom_pull(task_ids='extract')
    transformed = [{'id': item['id'], 'value': item['value'] * 2}
                   for item in data]
    return transformed

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline example',
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_from_api
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True
    )

    load = PostgresOperator(
        task_id='load',
        postgres_conn_id='postgres_default',
        sql="""
            INSERT INTO target_table (id, value)
            VALUES {{ task_instance.xcom_pull(task_ids='transform') }}
        """
    )

    extract >> transform >> load
```

### 示例 2: Prefect 数据管道

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract_data(source: str):
    """从数据源提取数据"""
    df = pd.read_csv(source)
    return df

@task
def clean_data(df: pd.DataFrame):
    """清洗数据"""
    df = df.dropna()
    df = df.drop_duplicates()
    return df

@task
def transform_data(df: pd.DataFrame):
    """转换数据"""
    df['value'] = df['value'] * 2
    df['category'] = df['category'].str.upper()
    return df

@task
def load_data(df: pd.DataFrame, destination: str):
    """加载数据到目标"""
    df.to_csv(destination, index=False)
    return len(df)

@flow(name="data-pipeline")
def data_pipeline(source: str, destination: str):
    """完整的数据管道"""
    raw_data = extract_data(source)
    cleaned_data = clean_data(raw_data)
    transformed_data = transform_data(cleaned_data)
    rows_loaded = load_data(transformed_data, destination)

    return f"Successfully loaded {rows_loaded} rows"

if __name__ == "__main__":
    data_pipeline(
        source="data/input.csv",
        destination="data/output.csv"
    )
```

### 示例 3: Temporal 微服务编排

```python
from temporalio import workflow, activity
from datetime import timedelta

@activity.defn
async def process_payment(order_id: str, amount: float):
    """处理支付"""
    # 调用支付服务
    print(f"Processing payment for order {order_id}: ${amount}")
    return {"status": "success", "transaction_id": "txn_123"}

@activity.defn
async def update_inventory(order_id: str, items: list):
    """更新库存"""
    print(f"Updating inventory for order {order_id}")
    return {"status": "updated"}

@activity.defn
async def send_notification(order_id: str, email: str):
    """发送通知"""
    print(f"Sending notification to {email} for order {order_id}")
    return {"status": "sent"}

@workflow.defn
class OrderWorkflow:
    @workflow.run
    async def run(self, order_id: str, amount: float, items: list, email: str):
        # 处理支付
        payment_result = await workflow.execute_activity(
            process_payment,
            args=[order_id, amount],
            start_to_close_timeout=timedelta(seconds=30),
        )

        if payment_result["status"] != "success":
            raise Exception("Payment failed")

        # 更新库存
        await workflow.execute_activity(
            update_inventory,
            args=[order_id, items],
            start_to_close_timeout=timedelta(seconds=30),
        )

        # 发送通知
        await workflow.execute_activity(
            send_notification,
            args=[order_id, email],
            start_to_close_timeout=timedelta(seconds=30),
        )

        return {"order_id": order_id, "status": "completed"}
```

## 🐛 常见问题

### 1. 如何选择合适的工作流引擎？

**考虑因素**:
```markdown
1. **使用场景**: 数据管道、微服务编排、业务流程？
2. **技术栈**: 团队熟悉的编程语言
3. **规模**: 任务数量、并发度、数据量
4. **部署环境**: 云、本地、Kubernetes
5. **预算**: 开源、商业、托管服务
```

### 2. 工作流引擎性能问题

**症状**: 任务执行缓慢、调度延迟

**解决方案**:
```markdown
- **增加资源**: 扩展 worker 数量
- **优化任务**: 减少任务粒度，避免过度依赖
- **使用缓存**: 缓存中间结果
- **并行执行**: 利用并行能力
- **监控调优**: 使用监控工具找出瓶颈
```

### 3. 工作流失败处理

**症状**: 任务失败后如何恢复

**解决方案**:
```markdown
- **自动重试**: 配置重试策略
- **告警通知**: 设置失败告警
- **幂等性**: 确保任务可重复执行
- **检查点**: 保存中间状态
- **手动干预**: 提供手动重试机制
```

### 4. 工作流监控和调试

**症状**: 难以追踪工作流执行状态

**解决方案**:
```markdown
- **日志记录**: 详细的日志输出
- **可视化**: 使用 UI 查看工作流
- **指标监控**: 收集执行指标
- **追踪系统**: 集成分布式追踪
- **告警系统**: 设置关键指标告警
```

## 📖 学习资源

### 官方文档

- **Airflow**: https://airflow.apache.org/docs/
- **Prefect**: https://docs.prefect.io/
- **Temporal**: https://docs.temporal.io/
- **Argo Workflows**: https://argoproj.github.io/workflows/
- **Dagster**: https://docs.dagster.io/
- **Camunda**: https://docs.camunda.org/

### 教程和示例

- **Airflow 教程**: https://github.com/apache/airflow/tree/main/airflow/example_dags
- **Prefect 示例**: https://github.com/PrefectHQ/prefect/tree/main/examples
- **Temporal 示例**: https://github.com/temporalio/samples-python

### 社区资源

- **Awesome Workflow Engines**: https://github.com/meirwah/awesome-workflow-engines
- **工作流引擎对比**: https://github.com/common-workflow-language/common-workflow-language
- **最佳实践**: 各引擎官方文档的最佳实践部分

## 📖 参考资料

- **GitHub 仓库**: https://github.com/meirwah/awesome-workflow-engines
- **工作流模式**: http://www.workflowpatterns.com/
- **BPMN 规范**: https://www.omg.org/spec/BPMN/

## 📝 更新日志

### v0.2.0 (2026-01-26)
- ✨ 更新到最新版本 (202f3b9)
- 📝 完善文档和引擎分类
- ✨ 添加详细的引擎介绍
- ✨ 添加选择指南和对比
- ✨ 添加实用示例代码
- ✨ 添加常见问题解答

### v0.1.0 (2026-01-25)
- 🎉 初始版本
