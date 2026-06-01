# Step Test Migration Map

Migration from step-numbered test files to domain-oriented suites.

## Source Files (25 total, ~1088 tests)

### test_steps_53_56.py
| Class | Tests | Target |
|-------|-------|--------|
| TestContinueFromNodeProjectLinking | 5 | orchestration/test_approval_queue.py |
| TestPatchRevert | 8 | orchestration/test_source_apply.py |
| TestChangeSet | 6 | orchestration/test_source_apply.py |

### test_steps_57_59.py
| Class | Tests | Target |
|-------|-------|--------|
| TestBrainGraphStructure | 8 | orchestration/test_project_brain.py |
| TestBrainReliabilityHygiene | 6 | orchestration/test_project_brain.py |
| TestCausalAccuracy | 2 | orchestration/test_project_brain.py |
| TestContinueFromNodeIntegration | 3 | orchestration/test_approval_queue.py |

### test_steps_68_1_69_70_71.py
| Class | Tests | Target |
|-------|-------|--------|
| TestEventSchemaRegistry | 12 | orchestration/test_event_ledger.py |
| TestDecisionQueue | 9 | orchestration/test_approval_queue.py |
| TestDashboard | 5 | ui_server/test_dashboard_contract.py |
| TestContextOptimizer | 5 | orchestration/test_project_brain.py |
| TestBrainIntegration | 5 | orchestration/test_project_brain.py |
| TestBrainDetail | 2 | ui_server/test_brain_view_model.py |
| TestTokenPolicyApplied | 3 | storage/test_persistence.py |

### test_steps_71_1_72_73_74.py
| Class | Tests | Target |
|-------|-------|--------|
| TestTokenPolicyAppliedSchema | 3 | storage/test_persistence.py |
| TestVisualSystem | 10 | ui_contracts/test_graph_architecture.py |
| TestBrainViewerShell | 14 | ui_contracts/test_responsive.py |

### test_steps_74_1_75_76_77_78_79.py
| Class | Tests | Target |
|-------|-------|--------|
| TestRedactionPatterns | 10 | ui_server/test_auth_redaction.py |
| TestInteractiveControls | 14 | ui_contracts/test_responsive.py |
| TestSpatialLayout | 7 | ui_contracts/test_graph_architecture.py |
| TestMotionDepth | 11 | ui_contracts/test_ux_quality.py |
| TestGuidanceRail | 8 | ui_contracts/test_responsive.py |

### test_steps_80_81_82.py
| Class | Tests | Target |
|-------|-------|--------|
| TestUIServer | 9 | ui_server/test_dashboard_contract.py |
| TestUIServerIntegration | 16 | ui_server/test_live_state.py |
| TestCalmEntryUX | 14 | ui_contracts/test_ux_quality.py |
| TestProgressiveBrainExplorer | 7 | ui_contracts/test_responsive.py |

### test_steps_83_90.py
| Class | Tests | Target |
|-------|-------|--------|
| TestBrainViewModel | 8 | ui_server/test_brain_view_model.py |
| TestNodeDetail | 2 | ui_server/test_brain_view_model.py |
| TestFrontendBuild | 3 | ui_contracts/test_responsive.py |
| TestUXAntiRegression | 9 | ui_contracts/test_ux_quality.py |
| TestUICommands | 2 | cli/test_command_catalog.py |
| TestLegacyViewerQuarantine | 2 | ui_contracts/test_responsive.py |
| TestServerEndpoints | 4 | ui_server/test_live_state.py |
| TestSessionRegistry | 3 | ui_server/test_live_state.py |

### test_steps_91_100.py
| Class | Tests | Target |
|-------|-------|--------|
| TestELKLayout | 8 | ui_contracts/test_graph_architecture.py |
| TestSemanticZoomV2 | 4 | ui_contracts/test_graph_architecture.py |
| TestScreenSpaceLabels | 3 | ui_contracts/test_ux_quality.py |
| TestExplainableEdges | 4 | ui_contracts/test_graph_architecture.py |
| TestLiveGrowth | 4 | ui_server/test_live_state.py |
| TestRemedyDo | 5 | cli/test_job_commands.py |
| TestSourceContext | 5 | orchestration/test_source_apply.py |
| TestStructuredPatch | 5 | orchestration/test_source_apply.py |
| TestSourceApply | 8 | orchestration/test_source_apply.py |
| TestFrontendBuildV2 | 3 | ui_contracts/test_responsive.py |

### test_steps_101_110.py
| Class | Tests | Target |
|-------|-------|--------|
| TestSmokeContractReset | 11 | regression/test_named_bugs.py |
| TestSemanticZoomDirection | 4 | ui_contracts/test_graph_architecture.py |
| TestForwardFlowLayout | 2 | ui_contracts/test_graph_architecture.py |
| TestTaskProgressRibbon | 4 | ui_contracts/test_ux_quality.py |
| TestHumanNodeLabels | 2 | ui_contracts/test_ux_quality.py |
| TestAtmosphericMotion | 3 | ui_contracts/test_ux_quality.py |
| TestLiveGrowthUX | 4 | ui_server/test_live_state.py |
| TestReviewerLoop | 8 | orchestration/test_approval_queue.py |
| TestReviewCLI | 3 | cli/test_job_commands.py |
| TestSourceContextFinalization | 2 | orchestration/test_source_apply.py |

### test_steps_111_116.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep111_UICLIContract | 8 | cli/test_command_catalog.py |
| TestStep112_ResourceCleanup | 8 | storage/test_persistence.py |
| TestStep113_SemanticZoom | 7 | ui_contracts/test_graph_architecture.py |
| TestStep114_ForwardFlow | 7 | ui_contracts/test_graph_architecture.py |
| TestStep115_TaskRibbon | 9 | ui_contracts/test_ux_quality.py |
| TestStep116_AutocoderE2E | 7 | orchestration/test_autorun.py |

### test_steps_122_126.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep122_JobFocusedOrigin | 6 | cli/test_job_commands.py |
| TestStep123_ViewModelHardening | 15 | ui_server/test_brain_view_model.py |
| TestStep124_WorkerUnloadSchema | 4 | orchestration/test_command_discovery.py |
| TestStep125_AutocoderCalcFixture | 8 | orchestration/test_autorun.py |

### test_steps_127_134.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep127_TaskProgressContract | 13 | ui_contracts/test_ux_quality.py |
| TestStep128_SmokeClosure | 5 | regression/test_named_bugs.py |
| TestStep129_HeadlessHygiene | 3 | orchestration/test_test_runner.py |
| TestStep130_WorkerVRAMCleanup | 6 | orchestration/test_command_discovery.py |
| TestStep131_UXVisualContract | 8 | ui_contracts/test_ux_quality.py |
| TestStep132_NodeDetailEdgeMeaning | 9 | ui_server/test_brain_view_model.py |
| TestStep133_AutocoderFakeE2E | 10 | orchestration/test_autorun.py |

### test_steps_135_140.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep135_DoDirectContract | 9 | cli/test_job_commands.py |
| TestStep136_AutocoderFakeE2E | 8 | orchestration/test_autorun.py |
| TestStep137_SmokeClosure | 4 | regression/test_named_bugs.py |
| TestStep138_DevStatusHonesty | 4 | orchestration/test_autonomy.py |
| TestStep139_NextAction | 9 | orchestration/test_autonomy.py |

### test_steps_141_146.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep141_SafeTaskLabel | 9 | cli/test_job_commands.py |
| TestStep142_ContractHardening | 8 | ui_contracts/test_ux_quality.py |
| TestStep143_DevStatusCommitReadiness | 4 | orchestration/test_autonomy.py |
| TestStep144_SmokeClosure | 4 | regression/test_named_bugs.py |
| TestStep145_NextAction | 6 | orchestration/test_autonomy.py |

### test_steps_163_171.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep163MemoryCandidates | 6 | orchestration/test_project_brain.py |
| TestStep164Story | 4 | orchestration/test_project_brain.py |
| TestStep165HumanDetail | 3 | ui_server/test_brain_view_model.py |
| TestStep166JourneyLayout | 2 | ui_contracts/test_graph_architecture.py |
| TestStep167Layers | 4 | ui_contracts/test_graph_architecture.py |
| TestStep168Checklist | 5 | ui_contracts/test_ux_quality.py |
| TestStep169CopyDictionary | 6 | ui_contracts/test_ux_quality.py |
| TestStep170UXSmokeGate | 4 | ui_contracts/test_ux_quality.py |

### test_steps_172_201.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep172Quarantine | 7 | regression/test_named_bugs.py |
| TestStep173Spec | 5 | orchestration/test_project_brain.py |
| TestStep174Structure | 10 | orchestration/test_project_brain.py |
| TestStep175ApiAdapter | 6 | ui_server/test_live_state.py |
| TestStep176_179ShellComponents | 9 | ui_contracts/test_responsive.py |
| TestStep180_183Graph | 8 | ui_contracts/test_graph_architecture.py |
| TestStep184_188RightPanel | 6 | ui_contracts/test_responsive.py |
| TestStep189_191TimelineDetailLayers | 3 | ui_contracts/test_ux_quality.py |
| TestStep192_193Visual | 6 | ui_contracts/test_ux_quality.py |
| TestStep194HumanCopy | 5 | ui_contracts/test_ux_quality.py |
| TestStep196ServerIntegration | 3 | ui_server/test_live_state.py |
| TestGlobalForbiddenWords | 2 | regression/test_named_bugs.py |
| TestGlobalNoCDN | 2 | regression/test_named_bugs.py |
| TestStep200DocsDeprecation | 1 | regression/test_named_bugs.py |

### test_steps_208_226.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep227ContractMarkers | 1 | ui_contracts/test_responsive.py |
| TestStep228Dependencies | 5 | ui_contracts/test_graph_architecture.py |
| TestStep229ResponsiveShell | 3 | ui_contracts/test_responsive.py |
| TestStep230SingleRail | 2 | ui_contracts/test_responsive.py |
| TestForceGraph | 10 | ui_contracts/test_graph_architecture.py |
| TestStep240DataNormalization | 2 | ui_server/test_live_state.py |
| TestStep241RightPanel | 2 | ui_contracts/test_responsive.py |
| TestStep243UiStart | 2 | ui_contracts/test_responsive.py |
| TestNoPopupOnLoad | 1 | ui_contracts/test_ux_quality.py |

### test_steps_247_252.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep247 | 3 | ui_server/test_dashboard_contract.py |
| TestStep248 | 6 | ui_server/test_dashboard_contract.py |
| TestStep249 | 8 | ui_server/test_dashboard_contract.py |
| TestStep250 | 6 | ui_server/test_dashboard_contract.py |
| TestStep251 | 3 | ui_server/test_dashboard_contract.py |

### test_steps_253_260.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep253 | 4 | ui_server/test_dashboard_contract.py |
| TestStep254 | 4 | ui_server/test_dashboard_contract.py |
| TestStep255 | 3 | ui_server/test_dashboard_contract.py |
| TestStep256 | 4 | orchestration/test_autonomy.py |
| TestStep257 | 4 | orchestration/test_autonomy.py |
| TestStep258 | 3 | orchestration/test_autonomy.py |
| TestStep259 | 4 | orchestration/test_autonomy.py |

### test_steps_261_268.py
| Class | Tests | Target |
|-------|-------|--------|
| TestStep261 | 4 | orchestration/test_test_runner.py |
| TestStep262 | 4 | orchestration/test_test_runner.py |
| TestStep263 | 8 | orchestration/test_test_runner.py |
| TestStep264 | 4 | orchestration/test_test_runner.py |
| TestStep265 | 7 | orchestration/test_test_runner.py |
| TestStep266 | 4 | orchestration/test_test_runner.py |
| TestStep267 | 5 | orchestration/test_test_runner.py |

### test_step_61_brain_correctness.py
| Class | Tests | Target |
|-------|-------|--------|
| TestMultiProofCausalEdges | 3 | orchestration/test_project_brain.py |
| TestFileProvenanceChain | 3 | orchestration/test_project_brain.py |
| TestContinueRoundtripAggregate | 2 | orchestration/test_project_brain.py |

### test_step_62_1_hygiene.py
| Class | Tests | Target |
|-------|-------|--------|
| TestSharedSymbols | 3 | orchestration/test_project_brain.py |
| TestNoDuplicateSection | 1 | regression/test_named_bugs.py |
| TestBrainDetailRegistry | 4 | orchestration/test_project_brain.py |
| TestNoSilentSwallow | 2 | regression/test_named_bugs.py |

### test_step_63_evidence_memory.py
| Class | Tests | Target |
|-------|-------|--------|
| TestMemoryCardModel | 3 | orchestration/test_project_brain.py |
| TestCardManagement | 7 | orchestration/test_project_brain.py |
| TestLearnEvidence | 1 | orchestration/test_project_brain.py |
| TestBrainMemoryNodeSafe | 1 | orchestration/test_project_brain.py |

### test_step_64_65_worker_git.py
| Class | Tests | Target |
|-------|-------|--------|
| TestWorkerShow | 4 | orchestration/test_command_discovery.py |
| TestWorkerExplain | 2 | orchestration/test_command_discovery.py |
| TestWorkerBrainNode | 1 | orchestration/test_command_discovery.py |
| TestGitStatusReader | 7 | orchestration/test_autonomy.py |
| TestGitStatusCLI | 2 | cli/test_job_commands.py |
| TestGitStatusBrainNode | 4 | orchestration/test_project_brain.py |
| TestGitReadinessSignal | 2 | orchestration/test_autonomy.py |

### test_step_66_67_68_event_stop_autonomy.py
| Class | Tests | Target |
|-------|-------|--------|
| TestEventLedgerNormalize | 4 | orchestration/test_event_ledger.py |
| TestEventLedgerScope | 1 | orchestration/test_event_ledger.py |
| TestEventLedgerTimeline | 1 | orchestration/test_event_ledger.py |
| TestEventLedgerSummary | 1 | orchestration/test_event_ledger.py |
| TestEventLedgerExport | 1 | orchestration/test_event_ledger.py |
| TestEventLedgerBrainNode | 1 | orchestration/test_event_ledger.py |
| TestEventCLIHelp | 2 | cli/test_command_catalog.py |
| TestStopReasonsCRUD | 3 | orchestration/test_autonomy.py |
| TestStopReasonsDerive | 3 | orchestration/test_autonomy.py |
| TestStopReasonExport | 1 | orchestration/test_autonomy.py |
| TestStopReasonBrainNode | 1 | orchestration/test_project_brain.py |
| TestBlockerCLIHelp | 1 | cli/test_command_catalog.py |
| TestAutonomyLoopBasic | 4 | orchestration/test_autonomy.py |
| TestAutonomyLoopExport | 2 | orchestration/test_autonomy.py |

## Target Summary

| Domain File | Source Classes | Est. Tests |
|-------------|---------------|------------|
| orchestration/test_source_apply.py | 7 classes | ~34 |
| orchestration/test_approval_queue.py | 4 classes | ~25 |
| orchestration/test_autorun.py | 4 classes | ~33 |
| orchestration/test_test_runner.py | 10 classes | ~39 |
| orchestration/test_command_discovery.py | 4 classes | ~13 |
| orchestration/test_autonomy.py | 14 classes | ~55 |
| orchestration/test_event_ledger.py | 7 classes | ~22 |
| orchestration/test_project_brain.py | 18 classes | ~76 |
| ui_server/test_dashboard_contract.py | 9 classes | ~56 |
| ui_server/test_live_state.py | 8 classes | ~42 |
| ui_server/test_brain_view_model.py | 6 classes | ~44 |
| ui_server/test_auth_redaction.py | 1 class | ~10 |
| cli/test_command_catalog.py | 7 classes | ~22 |
| cli/test_job_commands.py | 6 classes | ~34 |
| ui_contracts/test_graph_architecture.py | 13 classes | ~88 |
| ui_contracts/test_ux_quality.py | 16 classes | ~117 |
| ui_contracts/test_responsive.py | 14 classes | ~73 |
| storage/test_persistence.py | 4 classes | ~14 |
| regression/test_named_bugs.py | 13 classes | ~50 |
