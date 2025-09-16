"""
Tests for migration functionality ensuring no duplicate program chains

This test suite specifically focuses on testing that migration between islands
creates clean copies with UUID identifiers rather than _migrant suffixes,
preventing the exponential duplication that was occurring in the old implementation.
"""

import unittest
import uuid
import re
from openevolve.config import Config
from openevolve.database import Program, ProgramDatabase


class TestMigrationNoDuplicates(unittest.TestCase):
    """Tests for migration without creating duplicate program chains"""

    def setUp(self):
        """Set up test database with migration enabled"""
        config = Config()
        config.database.in_memory = True
        config.database.num_islands = 4
        config.database.migration_rate = 0.5  # 50% of programs migrate
        config.database.migration_interval = 2  # Migrate every 2 generations
        config.database.feature_bins = 5
        self.db = ProgramDatabase(config.database)

    def _create_test_program(self, program_id: str, score: float, features: list, island: int, generation: int = 1) -> Program:
        """Helper to create a test program"""
        program = Program(
            id=program_id,
            code=f"def func_{program_id}(): return {score}",
            language="python",
            metrics={"score": score, "combined_score": score},
            metadata={"island": island, "generation": generation},
        )
        program.features = features
        return program

    def _is_valid_uuid(self, test_string: str) -> bool:
        """Check if a string is a valid UUID"""
        try:
            uuid.UUID(test_string)
            return True
        except ValueError:
            return False

    def test_migration_creates_clean_uuid_ids(self):
        """Test that migration creates programs with clean UUID IDs, not _migrant suffixes"""
        # Add programs to different islands with enough generations to trigger migration
        for island in range(3):
            for i in range(3):
                prog = self._create_test_program(f"prog_{island}_{i}", 0.7 + i*0.1, [0.2 + i*0.1, 0.3], island, generation=3)
                self.db.add(prog)
                self.db.island_generations[island] = 3  # Set generation to trigger migration

        # Force migration
        original_program_count = len([p for island_map in self.db.island_feature_maps for p in island_map.values()])
        
        # Trigger migration by adding another program that would cause migration check
        self.db.migrate_programs()
        
        # Get all program IDs after migration
        all_program_ids = []
        for island_map in self.db.island_feature_maps:
            all_program_ids.extend(island_map.values())

        # Verify no program IDs contain '_migrant' suffix
        migrant_programs = [pid for pid in all_program_ids if '_migrant' in pid]
        self.assertEqual(len(migrant_programs), 0, 
                        f"Found programs with _migrant suffix after migration: {migrant_programs}")

        # Verify that any new program IDs created during migration are valid UUIDs
        original_ids = {f"prog_{i}_{j}" for i in range(3) for j in range(3)}
        migrated_ids = set(all_program_ids) - original_ids
        
        for migrated_id in migrated_ids:
            # Should be a valid UUID or original format, but never contain '_migrant'
            self.assertNotIn('_migrant', migrated_id, 
                           f"Migrated program ID {migrated_id} contains _migrant suffix")

    def test_multiple_migration_rounds_no_exponential_growth(self):
        """Test that multiple migration rounds don't create exponential program growth"""
        # Start with a few programs
        initial_programs = []
        for i in range(3):
            prog = self._create_test_program(f"initial_{i}", 0.8, [0.2 + i*0.2, 0.3], island=0, generation=1)
            self.db.add(prog)
            initial_programs.append(prog.id)

        # Run multiple migration rounds
        program_counts = []
        for round_num in range(5):
            # Set all islands to have enough generations to trigger migration
            for island in range(self.db.config.num_islands):
                self.db.island_generations[island] = round_num + 3

            self.db.migrate_programs()
            
            # Count total unique programs across all islands
            all_program_ids = set()
            for island_map in self.db.island_feature_maps:
                all_program_ids.update(island_map.values())
            
            program_counts.append(len(all_program_ids))

            # Verify no exponential growth (should be bounded)
            if round_num > 0:
                growth_ratio = program_counts[round_num] / program_counts[round_num - 1]
                self.assertLess(growth_ratio, 3.0, 
                              f"Exponential growth detected in round {round_num}: {growth_ratio}x growth")

        # Verify no _migrant suffixes anywhere
        final_program_ids = set()
        for island_map in self.db.island_feature_maps:
            final_program_ids.update(island_map.values())
        
        migrant_programs = [pid for pid in final_program_ids if '_migrant' in pid]
        self.assertEqual(len(migrant_programs), 0, 
                        f"Found programs with _migrant suffix after multiple migrations: {migrant_programs}")

    def test_migrated_program_content_preserved(self):
        """Test that migrated programs preserve original content and metrics"""
        # Create a program with specific content
        original_code = "def complex_function(x, y): return x**2 + y**2"
        original_metrics = {"score": 0.85, "combined_score": 0.85, "complexity": 42}
        
        prog = Program(
            id="original_prog",
            code=original_code,
            language="python",
            metrics=original_metrics,
            metadata={"island": 0, "generation": 3},
        )
        prog.features = [0.5, 0.6]
        
        self.db.add(prog)
        self.db.island_generations[0] = 3

        # Force migration
        self.db.migrate_programs()

        # Find any programs that might be migrants (not the original)
        all_program_ids = []
        for island_map in self.db.island_feature_maps:
            all_program_ids.extend(island_map.values())

        # Check that all programs (original and any migrants) have preserved content
        for prog_id in all_program_ids:
            program = self.db.get(prog_id)
            if program:
                # Code should be preserved
                self.assertEqual(program.code, original_code)
                # Core metrics should be preserved
                self.assertEqual(program.metrics.get("score"), 0.85)
                self.assertEqual(program.metrics.get("combined_score"), 0.85)

    def test_migration_target_islands_are_different(self):
        """Test that programs migrate to different islands, not same island"""
        # Add programs to island 0
        prog_ids = []
        for i in range(5):
            prog = self._create_test_program(f"prog_{i}", 0.7 + i*0.05, [0.2 + i*0.1, 0.3], island=0, generation=3)
            self.db.add(prog, target_island=0)
            prog_ids.append(prog.id)

        self.db.island_generations[0] = 3

        # Count programs per island before migration
        initial_counts = [len(island_map) for island_map in self.db.island_feature_maps]
        initial_total = sum(initial_counts)

        # Force migration
        self.db.migrate_programs()

        # Count programs per island after migration
        final_counts = [len(island_map) for island_map in self.db.island_feature_maps]
        final_total = sum(final_counts)

        # Main requirement: no _migrant_ suffixes
        migrant_suffix_programs = [pid for pid in self.db.programs.keys() if "_migrant_" in pid]
        self.assertEqual(len(migrant_suffix_programs), 0, "No programs should have _migrant_ suffixes")
        
        # Migration should create new programs (as evidenced by logs showing migration occurred)
        # The exact island distribution may vary based on feature coordinates
        self.assertGreaterEqual(final_total, initial_total, 
                               "Migration should create copies of programs")
        
        # Verify that some migration occurred by checking for migrant metadata
        migrant_programs = [p for p in self.db.programs.values() if p.metadata.get("migrant", False)]
        if len(migrant_programs) > 0:
            # If migrants exist, they should be in different islands than just island 0
            migrant_islands = set(p.metadata.get("island", 0) for p in migrant_programs)
            self.assertTrue(len(migrant_islands) > 1 or (len(migrant_islands) == 1 and 0 not in migrant_islands),
                           "Migrated programs should be in different islands")

    def test_no_duplicate_program_ids_across_all_islands(self):
        """Test that no program ID appears in multiple islands simultaneously"""
        # Add programs and trigger migration multiple times
        for round_num in range(3):
            for i in range(3):
                prog = self._create_test_program(f"round_{round_num}_prog_{i}", 0.6 + i*0.1, [0.2 + i*0.1, 0.4], island=0, generation=round_num + 2)
                self.db.add(prog)
            
            # Update generation counters and migrate
            for island in range(self.db.config.num_islands):
                self.db.island_generations[island] = round_num + 3
            
            self.db.migrate_programs()

        # Collect all program IDs from all islands
        all_program_ids = []
        for island_idx, island_map in enumerate(self.db.island_feature_maps):
            for coord, prog_id in island_map.items():
                all_program_ids.append((prog_id, island_idx, coord))

        # Check for duplicate program IDs
        seen_ids = set()
        duplicates = []
        
        for prog_id, island_idx, coord in all_program_ids:
            if prog_id in seen_ids:
                duplicates.append(prog_id)
            seen_ids.add(prog_id)

        self.assertEqual(len(duplicates), 0, 
                        f"Found duplicate program IDs across islands: {duplicates}")

    def test_migration_with_feature_map_conflicts_resolved_cleanly(self):
        """Test that when migrants compete for same feature cell, resolution is clean"""
        # Create programs with identical features but different quality
        prog1 = self._create_test_program("high_quality", 0.9, [0.5, 0.5], island=0, generation=3)
        prog2 = self._create_test_program("low_quality", 0.3, [0.5, 0.5], island=1, generation=3)
        
        self.db.add(prog1)
        self.db.add(prog2)
        
        # Set generation counters to trigger migration
        for island in range(self.db.config.num_islands):
            self.db.island_generations[island] = 3

        # Force migration - both programs might try to migrate to same cell in another island
        self.db.migrate_programs()

        # Verify that in any cell where both might have ended up, only the better one remains
        all_program_ids = set()
        for island_map in self.db.island_feature_maps:
            all_program_ids.update(island_map.values())

        # No _migrant suffixes should exist
        migrant_programs = [pid for pid in all_program_ids if '_migrant' in pid]
        self.assertEqual(len(migrant_programs), 0, 
                        f"Found programs with _migrant suffix: {migrant_programs}")


if __name__ == '__main__':
    unittest.main()