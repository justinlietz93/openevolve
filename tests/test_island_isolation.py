"""
Tests for worker-to-island pinning to ensure true island isolation
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import asyncio

from openevolve.config import Config, DatabaseConfig, EvaluatorConfig
from openevolve.database import ProgramDatabase, Program
from openevolve.process_parallel import ProcessParallelController


class TestIslandIsolation(unittest.TestCase):
    """Test that workers are properly pinned to islands"""

    def setUp(self):
        """Set up test environment"""
        self.config = Config()
        self.config.database.num_islands = 3
        self.config.evaluator.parallel_evaluations = 6  # 2 workers per island
        self.config.database.population_size = 30
        
        self.database = ProgramDatabase(self.config.database)
        self.evaluation_file = "mock_evaluator.py"

    def test_worker_island_mapping(self):
        """Test that workers are correctly mapped to islands"""
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Check mapping is correct
        expected_mapping = {
            0: 0,  # Worker 0 -> Island 0
            1: 1,  # Worker 1 -> Island 1
            2: 2,  # Worker 2 -> Island 2
            3: 0,  # Worker 3 -> Island 0
            4: 1,  # Worker 4 -> Island 1
            5: 2,  # Worker 5 -> Island 2
        }
        
        self.assertEqual(controller.worker_island_map, expected_mapping)

    def test_uneven_worker_distribution(self):
        """Test mapping when workers don't divide evenly into islands"""
        self.config.evaluator.parallel_evaluations = 7  # Not divisible by 3
        
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Island 0 should get 3 workers, islands 1 and 2 get 2 each
        island_worker_counts = {0: 0, 1: 0, 2: 0}
        for worker_id, island_id in controller.worker_island_map.items():
            island_worker_counts[island_id] += 1
        
        self.assertEqual(island_worker_counts[0], 3)
        self.assertEqual(island_worker_counts[1], 2)
        self.assertEqual(island_worker_counts[2], 2)

    def test_submit_iteration_uses_correct_island(self):
        """Test that _submit_iteration samples from the specified island"""
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Add some test programs to different islands
        for i in range(9):
            program = Program(
                id=f"test_prog_{i}",
                code=f"# Test program {i}",
                metrics={"combined_score": 0.5}
            )
            island_id = i % 3
            program.metadata["island"] = island_id
            self.database.add(program)
            self.database.islands[island_id].add(program.id)
        
        with patch.object(controller, 'executor') as mock_executor:
            mock_future = MagicMock()
            mock_executor.submit.return_value = mock_future
            
            # Submit iteration for island 1
            original_island = self.database.current_island
            future = controller._submit_iteration(100, island_id=1)
            
            # Check that database island was temporarily changed
            # but restored after sampling
            self.assertEqual(self.database.current_island, original_island)
            
            # Check that submit was called
            self.assertIsNotNone(future)
            mock_executor.submit.assert_called_once()
            
            # Get the snapshot that was passed to worker
            call_args = mock_executor.submit.call_args[0]
            db_snapshot = call_args[2]  # Third argument is db_snapshot
            
            # Verify snapshot has island marking
            self.assertEqual(db_snapshot["sampling_island"], 1)

    def test_island_isolation_during_evolution(self):
        """Test that parallel workers maintain island isolation"""
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Track which islands were sampled
        sampled_islands = []
        
        def mock_sample(num_inspirations=None):
            # Record which island was sampled
            sampled_islands.append(self.database.current_island)
            # Return mock parent and inspirations
            mock_program = Program(id="mock", code="", metrics={})
            return mock_program, []
        
        with patch.object(self.database, 'sample', side_effect=mock_sample):
            with patch.object(controller, 'executor'):
                # Submit iterations for different islands
                controller._submit_iteration(1, island_id=0)
                controller._submit_iteration(2, island_id=1)
                controller._submit_iteration(3, island_id=2)
                controller._submit_iteration(4, island_id=0)
                
                # Check that correct islands were sampled
                self.assertEqual(sampled_islands, [0, 1, 2, 0])

    def test_fewer_workers_than_islands(self):
        """Test handling when there are fewer workers than islands"""
        self.config.evaluator.parallel_evaluations = 2  # Only 2 workers for 3 islands
        
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Workers should be distributed across available islands
        expected_mapping = {
            0: 0,  # Worker 0 -> Island 0
            1: 1,  # Worker 1 -> Island 1
            # Island 2 has no dedicated worker
        }
        
        self.assertEqual(controller.worker_island_map, expected_mapping)

    def test_database_current_island_restoration(self):
        """Test that database current_island is properly restored after sampling"""
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Add test programs
        for i in range(6):
            program = Program(
                id=f"test_prog_{i}",
                code=f"# Test program {i}",
                metrics={"combined_score": 0.5}
            )
            island_id = i % 3
            program.metadata["island"] = island_id
            self.database.add(program)
            self.database.islands[island_id].add(program.id)
        
        # Set initial island
        self.database.current_island = 1
        original_island = self.database.current_island
        
        with patch.object(controller, 'executor') as mock_executor:
            mock_executor.submit.return_value = MagicMock()
            
            # Submit iteration for different island
            controller._submit_iteration(100, island_id=2)
            
            # Check that current_island was restored
            self.assertEqual(self.database.current_island, original_island)

    def test_island_distribution_in_batch(self):
        """Test that initial batch is distributed across islands"""
        controller = ProcessParallelController(
            self.config, self.evaluation_file, self.database
        )
        
        # Add test programs
        for i in range(9):
            program = Program(
                id=f"test_prog_{i}",
                code=f"# Test program {i}",
                metrics={"combined_score": 0.5}
            )
            island_id = i % 3
            program.metadata["island"] = island_id
            self.database.add(program)
            self.database.islands[island_id].add(program.id)
        
        # Track submitted islands
        submitted_islands = []
        
        def mock_submit_iteration(iteration, island_id=None):
            if island_id is not None:
                submitted_islands.append(island_id)
            return MagicMock()
        
        # Start the process pool
        controller.start()
        
        try:
            with patch.object(controller, '_submit_iteration', side_effect=mock_submit_iteration):
                # Start evolution with small batch to test distribution
                asyncio.run(controller.run_evolution(1, 6))  # 6 iterations
                
                # Check that islands were distributed (expect round-robin pattern)
                # Should be [0, 1, 2, 0, 1, 2] or similar distribution
                island_counts = {0: 0, 1: 0, 2: 0}
                for island_id in submitted_islands:
                    island_counts[island_id] += 1
                
                # Each island should have received iterations
                for count in island_counts.values():
                    self.assertGreater(count, 0)
        finally:
            controller.stop()


class TestIslandMigration(unittest.TestCase):
    """Test that migration still works with island pinning"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = Config()
        self.config.database.num_islands = 3
        self.config.database.migration_interval = 10
        self.config.database.migration_rate = 0.1
        self.database = ProgramDatabase(self.config.database)
    
    def test_migration_preserves_island_structure(self):
        """Test that migration works correctly with pinned workers"""
        # Add programs to islands properly
        for i in range(30):
            program = Program(
                id=f"prog_{i}",
                code=f"# Program {i}",
                metrics={"combined_score": i * 0.1}
            )
            island_id = i % 3
            program.metadata["island"] = island_id
            
            # Add to database
            self.database.programs[program.id] = program
            # Add to island
            self.database.islands[island_id].add(program.id)
        
        # Record island populations before migration
        island_sizes_before = [len(island) for island in self.database.islands]
        original_program_count = len(self.database.programs)
        
        # Verify we set up the test correctly
        self.assertEqual(sum(island_sizes_before), 30)
        self.assertEqual(original_program_count, 30)
        
        # Trigger migration
        self.database.migrate_programs()
        
        # Check islands still have programs
        island_sizes_after = [len(island) for island in self.database.islands]
        total_programs_after = len(self.database.programs)
        
        # All islands should still have programs
        for size in island_sizes_after:
            self.assertGreater(size, 0)
        
        # Migration creates copies, so total population should increase
        # With migration_rate=0.1 and 10 programs per island, expect ~1 program per island to migrate
        # Each program migrates to 2 adjacent islands, so we expect ~6 new programs
        self.assertGreater(total_programs_after, original_program_count)
        self.assertGreater(sum(island_sizes_after), sum(island_sizes_before))
        
        # Verify that migrant programs have correct metadata
        migrant_count = 0
        for program in self.database.programs.values():
            if program.metadata.get("migrant", False):
                migrant_count += 1
                # Migrant should have "_migrant_" in their ID
                self.assertIn("_migrant_", program.id)
        
        # Should have some migrant programs
        self.assertGreater(migrant_count, 0)


class TestWorkerPinningEdgeCases(unittest.TestCase):
    """Test edge cases for worker-to-island pinning"""
    
    def test_single_island(self):
        """Test behavior with only one island"""
        config = Config()
        config.database.num_islands = 1
        config.evaluator.parallel_evaluations = 4
        
        database = ProgramDatabase(config.database)
        controller = ProcessParallelController(config, "test.py", database)
        
        # All workers should map to island 0
        expected_mapping = {0: 0, 1: 0, 2: 0, 3: 0}
        self.assertEqual(controller.worker_island_map, expected_mapping)
    
    def test_single_worker(self):
        """Test behavior with only one worker"""
        config = Config()
        config.database.num_islands = 5
        config.evaluator.parallel_evaluations = 1
        
        database = ProgramDatabase(config.database)
        controller = ProcessParallelController(config, "test.py", database)
        
        # Single worker should map to island 0
        expected_mapping = {0: 0}
        self.assertEqual(controller.worker_island_map, expected_mapping)


if __name__ == "__main__":
    unittest.main()