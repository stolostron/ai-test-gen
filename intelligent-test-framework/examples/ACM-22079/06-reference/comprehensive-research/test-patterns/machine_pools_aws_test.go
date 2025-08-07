package machine_pools

import (
	"fmt"

	"github.com/onsi/ginkgo/v2"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("AWS Machine Pools", ginkgo.Label("machinepools"), func() {
	ginkgo.BeforeEach(func() {
		var cloudProvider = "aws"
		_, err := libgoclusters.GetHiveClusterNamespaces(Appliers, cloudProvider)
		if err != nil {
			ginkgo.Skip(fmt.Sprintf("Skipping test due to failure in GetHiveClusterNamespaces: %v", err))
		}
	})

	// Scale Up
	ginkgo.It("RHACM4K-24024 - As a cluster-admin with an ACM-created AWS cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24024", "scale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", false, 1, 0, 0, "", "")
	})

	// Scale Down
	ginkgo.It("RHACM4K-24030 - As a cluster-admin with an ACM-created AWS cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24030", "scale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", false, -1, 0, 0, "", "")
	})

	// Autoscale Up
	ginkgo.It("RHACM4K-24036 - As a cluster-admin with an ACM-created AWS cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24036", "autoscale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", true, 0, 1, 1, "", "")
	})

	// Autoscale Down
	ginkgo.It("RHACM4K-24048 - As a cluster-admin with an ACM-created AWS cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24048", "autoscale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", true, 0, -1, -1, "", "")
	})
})
